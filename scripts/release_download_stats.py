#!/usr/bin/env python3
# Copyright (C) 2026 Marcel Verpaalen
# SPDX-License-Identifier: GPL-3.0-or-later
# Licensed under the GNU General Public License v3.0 or later.
"""
Keep running download totals for the files of a rolling GitHub release.

GitHub counts downloads per uploaded asset, and the rolling releases replace
their files on every run (`gh release upload --clobber`), which starts a new
asset at 0 downloads. Run this just BEFORE a workflow uploads new files: it
reads each asset's current count, adds what is new since the previous
snapshot to a `download-stats.json` asset in the same release, and uploads
that file.

What is new is decided per asset id, so double counting cannot happen:
  - asset id seen last time: add (count - count at the last snapshot)
  - new asset id (file was replaced): add its whole count
Matching on the id (not the name) also covers the temporary names used by
publish_release_assets.py: an asset renamed to `<name>.previous` or uploaded
as `<name>.uploading` is counted under `<name>`, and never twice.
A region that failed to regenerate keeps its old asset and is counted
correctly on the next run. Downloads in the few seconds between the
snapshot and the upload are lost; that is the only gap.

download-stats.json:
  {"release": tag, "updated": ISO time,
   "totals": {"all": n, "files": {name: n}},
   "daily":  {"YYYY-MM-DD": {name: n}},   # new downloads seen at that day's snapshots
   "assets": {name: {"id": asset id, "count": count at snapshot}}}  # bookkeeping

download-stats.bak.json holds the previous version (see BACKUP_NAME).

Usage (needs the gh CLI, authenticated; GH_TOKEN in workflows):
    python3 release_download_stats.py TAG [--repo owner/name] [--dry-run]
    python3 release_download_stats.py --report [TAG ...]   # print totals

Stdlib only. Never fails the calling workflow on its own: errors are
reported and the exit code is 0 unless --strict is given.
"""

import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

STATS_NAME = "download-stats.json"
# Previous version, uploaded before STATS_NAME is replaced: `gh release
# upload --clobber` deletes the old asset before uploading the new one, so a
# failed upload would otherwise lose the totals. load_stats() falls back to it.
BACKUP_NAME = "download-stats.bak.json"
OWN_NAMES = (STATS_NAME, BACKUP_NAME)
# Temporary names used by publish_release_assets.py while replacing an asset
TEMP_SUFFIXES = (".uploading", ".previous")
DEFAULT_REPO = "marcelrv/OpenCPN-Waypoints"
KEEP_DAYS = 800


def gh_api(path: str, repo: str, accept: str = None) -> bytes:
    cmd = ["gh", "api", f"repos/{repo}/{path}"]
    if accept:
        cmd += ["-H", f"Accept: {accept}"]
    return subprocess.run(cmd, check=True, capture_output=True).stdout


def get_release(tag: str, repo: str):
    try:
        return json.loads(gh_api(f"releases/tags/{tag}", repo))
    except subprocess.CalledProcessError as e:
        if b"Not Found" in (e.stderr or b"") or b"404" in (e.stderr or b""):
            return None
        raise


def load_stats(release: dict, repo: str) -> tuple:
    """(stats, name of the asset they came from, or None). Falls back to the
    backup when the main file is missing or unusable (an earlier replacement
    failed half-way, or an upload left an incomplete asset). Starting from the
    backup is exact: its per-asset bookkeeping matches the counts it summed.
    Raises when stats exist but none can be read, rather than starting the
    totals again from zero."""
    by_name = {a["name"]: a for a in release.get("assets", [])}
    problems = []
    for name in OWN_NAMES:
        asset = by_name.get(name)
        if asset is None:
            continue
        try:
            if asset.get("state", "uploaded") != "uploaded":
                raise ValueError(f"asset state is {asset.get('state')}")
            stats = json.loads(gh_api(f"releases/assets/{asset['id']}", repo,
                                      "application/octet-stream"))
            if not isinstance(stats, dict) or "totals" not in stats:
                raise ValueError("not a stats file")
        except (ValueError, subprocess.CalledProcessError) as e:
            problems.append(f"{name}: {e}")
            print(f"  {name} unusable ({e})", file=sys.stderr)
            continue
        if name == BACKUP_NAME:
            print(f"  recovering from {BACKUP_NAME}", file=sys.stderr)
        return stats, name
    if problems:
        raise RuntimeError("no usable download stats: " + "; ".join(problems))
    return {}, None


def canonical_name(name: str) -> str:
    for suffix in TEMP_SUFFIXES:
        if name.endswith(suffix):
            return name[:-len(suffix)]
    return name


def update(stats: dict, release: dict, now: datetime) -> dict:
    """Add the downloads since the previous snapshot. Pure: no I/O, and
    `stats` is not modified (it is uploaded as the backup afterwards)."""
    stats = copy.deepcopy(stats)
    tag = release["tag_name"]
    totals = stats.get("totals", {}).get("files", {})
    # count at the last snapshot, per asset id
    seen = {v["id"]: v["count"] for v in stats.get("assets", {}).values()}
    daily = stats.get("daily", {})
    day = now.strftime("%Y-%m-%d")
    assets = {}
    for a in release.get("assets", []):
        asset_name, aid, count = a["name"], a["id"], int(a["download_count"])
        if asset_name in OWN_NAMES:
            continue
        name = canonical_name(asset_name)
        new = max(count - seen.get(aid, 0), 0)
        if new:
            totals[name] = totals.get(name, 0) + new
            daily.setdefault(day, {})
            daily[day][name] = daily[day].get(name, 0) + new
        totals.setdefault(name, totals.get(name, 0))
        assets[asset_name] = {"id": aid, "count": count}
    for old in sorted(daily)[:-KEEP_DAYS]:
        del daily[old]
    return {
        "release": tag,
        "updated": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "totals": {"all": sum(totals.values()), "files": dict(sorted(totals.items()))},
        "daily": dict(sorted(daily.items())),
        "assets": dict(sorted(assets.items())),
    }


def snapshot(tag: str, repo: str, dry_run: bool) -> None:
    release = get_release(tag, repo)
    if release is None:
        print(f"{tag}: release does not exist yet, nothing to count")
        return
    before, source = load_stats(release, repo)
    stats = update(before, release, datetime.now(timezone.utc))
    added = stats["totals"]["all"] - before.get("totals", {}).get("all", 0)
    print(f"{tag}: +{added} downloads since the last snapshot, {stats['totals']['all']} in total")
    if dry_run:
        print(json.dumps(stats["totals"], indent=2))
        return
    with tempfile.TemporaryDirectory() as d:
        # Back up the previous totals first; if that fails, nothing has been
        # replaced yet and the exception leaves the release untouched. When
        # recovering from the backup, it is the only copy: leave it alone and
        # only restore the main asset (the next run refreshes the backup).
        if before and source == STATS_NAME:
            upload(tag, repo, d, BACKUP_NAME, before)
        upload(tag, repo, d, STATS_NAME, stats)


def upload(tag: str, repo: str, d: str, name: str, data: dict) -> None:
    path = os.path.join(d, name)
    with open(path, "w") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
    subprocess.run(["gh", "release", "upload", tag, path, "--clobber", "--repo", repo],
                   check=True, capture_output=True)


def report(tags: list, repo: str) -> None:
    if not tags:
        tags = [r["tag_name"] for r in json.loads(gh_api("releases?per_page=100", repo))]
    for tag in tags:
        release = get_release(tag, repo)
        stats = load_stats(release, repo)[0] if release else {}
        if not stats:
            print(f"\n{tag}: no {STATS_NAME} yet")
            continue
        daily = stats.get("daily", {})
        last7 = sorted(daily)[-7:]
        print(f"\n{tag}: {stats['totals']['all']} downloads in total (updated {stats['updated']}); "
              f"last 7 snapshot days: {sum(sum(daily[d].values()) for d in last7)}")
        for name, n in sorted(stats["totals"]["files"].items(), key=lambda x: -x[1]):
            print(f"  {n:7d}  {name}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tags", nargs="*")
    ap.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPO))
    ap.add_argument("--report", action="store_true", help="print totals instead of taking a snapshot")
    ap.add_argument("--dry-run", action="store_true", help="compute but do not upload")
    ap.add_argument("--strict", action="store_true", help="exit non-zero on errors")
    args = ap.parse_args()
    try:
        if args.report:
            report(args.tags, args.repo)
        else:
            if len(args.tags) != 1:
                ap.error("give exactly one release tag")
            snapshot(args.tags[0], args.repo, args.dry_run)
    except Exception as e:  # stats must never block a data upload
        err = e.stderr.decode(errors="replace").strip() if isinstance(e, subprocess.CalledProcessError) and e.stderr else e
        print(f"download stats: {type(e).__name__}: {err}", file=sys.stderr)
        if args.strict:
            sys.exit(1)


if __name__ == "__main__":
    main()
