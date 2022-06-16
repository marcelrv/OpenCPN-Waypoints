# OpenCPN-Waypoints
GPX Files for OpenCPN

* [marrekrite.gpx](marrekrite.gpx)  - Alle marrekritten aanlegplaatsen for use with OpenCPN. Import as Layer so it can be easily switched on/off
* [Friesland-Bridges.gpx][Friesland-Bridges.gpx) -Alle Friese bruggen met openingstijden en marifoon kanaal
* [NL-Bridges.gpx](NL-Bridges.gpx) - Alle Nederlandse bruggen met openingstijden en marifoon kanaal 
* [BE-Bridges.gpx](BE-Bridges.gpx) - Belgische bruggen
* [DE-Bridges.gpx](DE-Bridges.gpx) - Duitse bruggen
* [AT-Bridges.gpx](AT-Bridges.gpx) - Oosterijkse bruggen
* [FR-Bridges.gpx](FR-Bridges.gpx) - Franse bruggen
* [CH-Bridges.gpx](CH-Bridges.gpx) - Zwitserse bruggen

![openCPN brug info image](./img/openCPN-brug.png)


# Tools
* [marrekritten_to_GPX.py](marrekritten_to_GPX.py) - File to automatically create marrekrite.gpx from the https://www.marrekrite.frl website.  
To update run `python3 marrekritten_to_GPX.py`

* [bridges.py](bridges.py) - File to automatically create NL-Bridges.gpx and BE & DE from the public data of Rijkswaterstaat on https://www.vaarweginformatie.nl/  
To update run `python3 bridges.py`

Requires gpxpy, you can install this with `pip3 install gpxpy`

The gpx file included is last updated March 2022 so should help you through the season.
