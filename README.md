# OpenCPN-Waypoints
GPX Files for OpenCPN

* [marrekrite.gpx](marrekrite.gpx)  - Alle marrekritten aanlegplaatsen for use with OpenCPN. Import as Layer so it can be easily switched on/off
* [NLBridges.gpx](NLBridges.gpx) - Alle Nederlandse bruggen met openingstijden en marifoon kanaal
![image](https://user-images.githubusercontent.com/5871213/173774589-dcffd332-2f87-4ccb-82a7-d8b150f98b89.png)


# Tools
* [marrekritten_to_GPX.py](marrekritten_to_GPX.py) - File to automatically create marrekrite.gpx from the https://www.marrekrite.frl website.  
To update run `python3 marrekritten_to_GPX.py`

* [bridges.py](bridges.py) - File to automatically create NLBridges.gpx from the public data of Rijkswaterstaat on https://www.vaarweginformatie.nl/  
To update run `python3 bridges.py`

Requires gpxpy, you can install this with `pip3 install gpxpy`

The gpx file included is last updated March 2022 so should help you through the season.
