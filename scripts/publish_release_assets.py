#!/usr/bin/env python3
# Copyright (C) 2026 Marcel Verpaalen
# SPDX-License-Identifier: GPL-3.0-or-later
# Licensed under the GNU General Public License v3.0 or later.
"""
Publish files to a single rolling GitHub release, replacing assets safely.

All files live in one release (default tag `waypoints-latest`), so every file
keeps a stable download link:
    https://github.com/<repo>/releases/download/<tag>/<name>

A failure must never leave a missing or empty file behind, so this does NOT
use `gh release upload --clobber` (that deletes the old asset first).
Per file:
  1. check the local file: not empty, a .gpx parses and has waypoints,
     a .zip passes a zip test; a bad file is skipped and the old asset kept
  2. upload it as `<name>.uploading` and check the uploaded size
  3. only then rename the old asset to `<name>.previous`, rename the new one
     to `<name>` and delete the previous one; when the rename fails, the
     previous asset is renamed back
Leftover `*.uploading` / `*.previous` assets of an interrupted run are cleaned
up first (renamed into place when `<name>` is missing, otherwise removed).

Remaining gap: asset names are unique, so `<name>` does not exist for the
moment between the two renames. If the job is killed exactly then, the link
fails until the next run restores the file from the leftovers.

The release is created (not marked as latest) when it does not exist yet.

Usage (needs the gh CLI, authenticated; GH_TOKEN in workflows):
    python3 publish_release_assets.py TAG FILE... [--list FILE] [--repo owner/name]

Exits non-zero when any file could not be published, so the workflow stops
before committing the updated chartInfo.json and the next run retries.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from xml.etree import ElementTree

DEFAULT_REPO = "marcelrv/OpenCPN-Waypoints"
TEMP_SUFFIX = ".uploading"
PREVIOUS_SUFFIX = ".previous"
GPX_NS = "{http://www.topografix.com/GPX/1/1}"
RELEASE_TITLE = "Waypoints (latest)"
RELEASE_NOTES = (
    "Always the latest generated GPX waypoint files and OpenCPN chart catalog zips. "
    "Files are replaced in place when their data changes; the download links stay the same. "
    "Download totals are kept in download-stats.json."
)


def gh(*args: str) -> bytes:
    return subprocess.run(["gh", *args], check=True, capture_output=True).stdout


def gh_api(path: str, repo: str, *args: str) -> bytes:
    return gh("api", f"repos/{repo}/{path}", *args)


def get_release(tag: str, repo: str):
    try:
        return json.loads(gh_api(f"releases/tags/{tag}", repo))
    except subprocess.CalledProcessError as e:
        if b"Not Found" in (e.stderr or b"") or b"404" in (e.stderr or b""):
            return None
        raise


def ensure_release(tag: str, repo: str) -> dict:
    release = get_release(tag, repo)
    if release is None:
        print(f"{tag}: creating release")
        gh("release", "create", tag, "--repo", repo, "--title", RELEASE_TITLE,
           "--notes", RELEASE_NOTES, "--latest=false")
        release = get_release(tag, repo)
        if release is None:
            raise RuntimeError(f"release {tag} not found after creating it")
    return release


def list_assets(release_id: int, repo: str) -> list:
    assets, page = [], 1
    while True:
        batch = json.loads(gh_api(f"releases/{release_id}/assets?per_page=100&page={page}", repo))
        assets += batch
        if len(batch) < 100:
            return assets
        page += 1


def delete_asset(asset_id: int, repo: str) -> None:
    gh_api(f"releases/assets/{asset_id}", repo, "-X", "DELETE")


def rename_asset(asset_id: int, name: str, repo: str) -> None:
    for attempt in range(3):
        try:
            gh_api(f"releases/assets/{asset_id}", repo, "-X", "PATCH", "-f", f"name={name}")
            return
        except subprocess.CalledProcessError:
            if attempt == 2:
                raise
            time.sleep(5)


def clean_leftovers(release_id: int, repo: str) -> None:
    """Handle the `*.uploading` / `*.previous` assets of an interrupted run.
    When `<name>` itself is missing, one of them is the only copy and is
    renamed into place: the new upload (it was verified before the old asset
    was moved aside), else the previous one. All other leftovers are removed."""
    assets = list_assets(release_id, repo)
    names = {a["name"] for a in assets}
    leftovers = {}
    for a in assets:
        for suffix in (TEMP_SUFFIX, PREVIOUS_SUFFIX):
            if a["name"].endswith(suffix):
                leftovers.setdefault(a["name"][:-len(suffix)], {})[suffix] = a
    for final, found in sorted(leftovers.items()):
        if final not in names:
            for suffix in (TEMP_SUFFIX, PREVIOUS_SUFFIX):
                a = found.get(suffix)
                if a is not None and a.get("state") == "uploaded":
                    print(f"  restoring {final} from leftover {a['name']}")
                    rename_asset(a["id"], final, repo)
                    del found[suffix]
                    break
        for a in found.values():
            print(f"  removing leftover {a['name']}")
            delete_asset(a["id"], repo)


def check_file(path: str) -> str:
    """Return a reason why the file must not be published, or ''."""
    if not os.path.isfile(path):
        return "file does not exist"
    if os.path.getsize(path) == 0:
        return "file is empty"
    try:
        if path.endswith(".gpx"):
            root = ElementTree.parse(path).getroot()
            if root.find(f"{GPX_NS}wpt") is None:
                return "GPX has no waypoints"
        elif path.endswith(".zip"):
            with zipfile.ZipFile(path) as z:
                if not z.namelist():
                    return "zip is empty"
                bad = z.testzip()
                if bad:
                    return f"zip member {bad} is corrupt"
                for member in z.namelist():
                    if member.endswith(".gpx"):
                        with z.open(member) as f:
                            if ElementTree.parse(f).getroot().find(f"{GPX_NS}wpt") is None:
                                return f"zip member {member} has no waypoints"
    except (ElementTree.ParseError, zipfile.BadZipFile, OSError) as e:
        return f"{type(e).__name__}: {e}"
    return ""


def publish_file(tag: str, repo: str, release_id: int, path: str, tmpdir: str) -> None:
    name = os.path.basename(path)
    temp_name = name + TEMP_SUFFIX
    temp_path = os.path.join(tmpdir, temp_name)
    shutil.copyfile(path, temp_path)
    gh("release", "upload", tag, temp_path, "--repo", repo)

    assets = {a["name"]: a for a in list_assets(release_id, repo)}
    new = assets.get(temp_name)
    size = os.path.getsize(path)
    if new is None or new.get("state") != "uploaded" or int(new["size"]) != size:
        if new is not None:
            delete_asset(new["id"], repo)
        raise RuntimeError(f"upload of {name} not complete (expected {size} bytes), old asset kept")

    old = assets.get(name)
    if old is not None:
        # keep the old asset as a recovery copy until the new one has its name
        rename_asset(old["id"], name + PREVIOUS_SUFFIX, repo)
    try:
        rename_asset(new["id"], name, repo)
    except Exception:
        if old is not None:
            rename_asset(old["id"], name, repo)
            delete_asset(new["id"], repo)
        raise
    if old is not None:
        delete_asset(old["id"], repo)
    print(f"  published {name} ({size} bytes)")


def check_catalogs(tag: str, repo: str, release, catalogs: list) -> int:
    """Every `zipfile_location` in the catalogs that points at this release
    must be an existing asset; otherwise the catalog must not be committed."""
    if not catalogs:
        return 0
    prefix = f"https://github.com/{repo}/releases/download/{tag}/"
    assets = {a["name"] for a in list_assets(release["id"], repo)} if release else set()
    missing = []
    for catalog in catalogs:
        for loc in ElementTree.parse(catalog).getroot().iter("zipfile_location"):
            url = (loc.text or "").strip()
            if url.startswith(prefix) and url[len(prefix):] not in assets:
                missing.append(f"{catalog}: {url[len(prefix):]}")
    if missing:
        print("error: the catalog links to files that are not in the release:\n  "
              + "\n  ".join(missing), file=sys.stderr)
        return 1
    print(f"catalog check: all release links in {', '.join(catalogs)} exist")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tag")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--list", help="file with one path per line to publish (in addition to FILES)")
    ap.add_argument("--check-catalog", action="append", default=[], metavar="XML",
                    help="after publishing, fail when a chart catalog links to a file of this release "
                         "that is not one of its assets (can be given more than once)")
    ap.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPO))
    args = ap.parse_args()

    files = list(args.files)
    if args.list:
        if not os.path.isfile(args.list):
            print(f"error: list file {args.list} does not exist", file=sys.stderr)
            return 1
        with open(args.list) as f:
            files += [line.strip() for line in f if line.strip()]
    files = list(dict.fromkeys(files))  # dedupe, keep order
    if not files:
        # still recover the assets of an interrupted earlier run
        release = get_release(args.tag, args.repo)
        if release is not None:
            clean_leftovers(release["id"], args.repo)
        print("nothing to publish")
        return check_catalogs(args.tag, args.repo, release, args.check_catalog)

    names = [os.path.basename(p) for p in files]
    if len(set(names)) != len(names):
        print("error: two files share the same name", file=sys.stderr)
        return 1

    release = ensure_release(args.tag, args.repo)
    clean_leftovers(release["id"], args.repo)

    failed = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for path in files:
            reason = check_file(path)
            if reason:
                print(f"  SKIPPED {path}: {reason}; old asset kept", file=sys.stderr)
                failed.append(path)
                continue
            try:
                publish_file(args.tag, args.repo, release["id"], path, tmpdir)
            except Exception as e:
                err = e.stderr.decode(errors="replace").strip() \
                    if isinstance(e, subprocess.CalledProcessError) and e.stderr else e
                print(f"  FAILED {path}: {err}", file=sys.stderr)
                failed.append(path)
    print(f"{args.tag}: published {len(files) - len(failed)} of {len(files)} files")
    if failed:
        print("not published: " + ", ".join(failed), file=sys.stderr)
        return 1
    return check_catalogs(args.tag, args.repo, release, args.check_catalog)


if __name__ == "__main__":
    sys.exit(main())
