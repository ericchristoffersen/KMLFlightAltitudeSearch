Aircraft Low Altitude KML Search

We have been having a lot of seaplanes flying very low over our town, and the FAA inspector wanted a list of tail numbers and the times when the low flying occured. I wrote this script to search plane's kml flight track files to find when they violated 19.119 with respect to a list of locations.

To use, download flight track kml files from flightaware to a directory on your computer.

Create a 'location file' that contain the locations you are concerned about with each location on its own line.

Location format is:

"location name", latitude, longitude, altitude in feet

For example create a file "locs.txt" that contains:

"beaux arts sailboat dock", 47.58407, -122.20493, 29

"beaux arts water tower, 10528 se 27th street, beaux arts", 47.586611, -122.199839, 300

"barnabie point community center, Mercer Island", 47.57695, -122.20374, 175

For example, there are sample files you can use, run the script as:

	python AltitudeFinder.py searchlocations.txt sample searchoutput.csv 2000 1000

Where 4th argument is horizontal distance from search location to plane and 5th argument is planes altitude.

Script will append to a csv all times and locations that are within 2000 feet of search location and within 1000 feet altitude of search location.

If you wish to search a single kml file then:

	python AltitudeFinder.py searchlocations.txt sample\sample.kml searchoutput2.csv 2000 1000

If you wish to search all kml in a directory for planes that fly even closer and lower you can decrease the distance and altitude limits:

	python AltitudeFinder.py searchlocations.txt sample\sample.kml searchoutput2.csv 1000 500

Output is a csv file that lists search locations in upper left of spreadsheet and below that all plane/time/location within search criteria.

LIMITATIONS:

The plane flight tracks are sets of points with an inferred LINE between them. Reported time, altitude and location are linearly interpolated from the points. A better implementation would use a cubic spline... In any case this is a tool to find potential violations, ultimately the FAA is the arbiter, send the data to them to decide.
