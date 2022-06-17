# OpenCPN-Waypoints
GPX Files for OpenCPN

* [marrekrite.gpx](marrekrite.gpx)  - Alle marrekritten aanlegplaatsen for use with OpenCPN. Import as Layer so it can be easily switched on/off
* [Friesland-Bruggen.gpx](Friesland-Bruggen.gpx) -Alle Friese bruggen met openingstijden en marifoon kanaal
* [NL-Bruggen.gpx](NL-Bruggen.gpx) - Alle Nederlandse bruggen met openingstijden en marifoon kanaal 
* [BE-Bruggen.gpx](BE-Bruggen.gpx) - Belgische bruggen
* [DE-Bruggen.gpx](DE-Bruggen.gpx) - Duitse bruggen
* [AT-Bruggen.gpx](AT-Bruggen.gpx) - Oosterijkse bruggen
* [FR-Bruggen.gpx](FR-Bruggen.gpx) - Franse bruggen
* [CH-Bruggen.gpx](CH-Bruggen.gpx) - Zwitserse bruggen

* [Friesland-Sluizen.gpx](Friesland-Sluizen.gpx) -Alle Friese sluizen met openingstijden en marifoon kanaal
* [NL-Sluizen.gpx](NL-Sluizen.gpx) - Alle Nederlandse sluizen met openingstijden en marifoon kanaal 
* [BE-Sluizen.gpx](BE-Sluizen.gpx) - Belgische sluizen
* [DE-Sluizen.gpx](DE-Sluizen.gpx) - Duitse sluizen
* [AT-Sluizen.gpx](AT-Sluizen.gpx) - Oosterijkse sluizen
* [FR-Sluizen.gpx](FR-Sluizen.gpx) - Franse sluizen

![openCPN brug info image](./img/openCPN-brug.png)

# Tools
* [marrekritten_to_GPX.py](marrekritten_to_GPX.py) - File to automatically create marrekrite.gpx from the https://www.marrekrite.frl website.  
To update run `python3 marrekritten_to_GPX.py`

* [bridges.py](bridges.py) - File to automatically create NL-Bridges.gpx and BE & DE from the public data of Rijkswaterstaat on https://www.vaarweginformatie.nl/  
To update run `python3 bridges.py`

Requires gpxpy, you can install this with `pip3 install gpxpy`

The gpx file included is last updated March 2022 so should help you through the season.
