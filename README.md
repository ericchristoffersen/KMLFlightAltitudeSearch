# Aircraft Low Altitude KML Search

We have been having a lot of seaplanes flying very low over our town, and the FAA inspector wanted a list of tail numbers and the times when the low flying occured. I wrote this script to search plane's kml flight track files to find when they violated 19.119 with respect to a list of locations.

To use, download flight track kml files from flightaware to a directory on your computer, then run script to find all locations on flight tracks that come within specificed distance limits.

## Examples

Here are some examples using the files included with the source.

### single kml file
If you wish to search a single kml file then:

<code>python AltitudeFinder.py searchlocations.txt sample\sample.kml searchoutput2.csv 2000 1000</code>

### directory of kml files

If you wish to search all kml in a directory called 'sample' for planes that fly even closer and lower you can decrease the distance and altitude limits:

<code>python AltitudeFinder.py searchlocations.txt sample searchoutput2.csv 1000 500</code>

### Example with results

<code>python AltitudeFinder.py searchlocations.txt sample searchoutput.csv 1500 500</code>

This searches the projects 'sample' directory for kml files, then reports each instance where a flight segment encroached within 1500ft of sample locations at relative altitude of less than 500'. Output is searchoutput.csv, that file can be opened in a spreadsheet program (for example google sheets) and will contain:

<table>
<thead>
<tr>
<th>search location name</th>
<th>location lat</th>
<th>location lon</th><th>location alt (ft)</th><th>kmltag</th><th>filename</th><th>time</th><th>location name</th><th>reported altitude (ft)</th><th>distance (ft)</th><th>altitude above location(ft)</th>
</tr>
</thead>
<tbody>
<tr>
<td>" beaux arts sailboat dock "</td><td>47.58407</td><td>-122.20493</td><td>28.999999999999996</td></tr>
<tr>
<td>" beaux arts water tower 10528 se 27th street, beaux arts "</td><td>47.586611</td><td>-122.199839</td><td>300.0</td>
</tr>
<tr>
<td>" barnabie point community center, Mercer Island "</td><td>47.57695</td><td>-122.20374</td><td>175.0</td>
</tr>
<tr>
<td></td><td></td><td></td><td></td><td>" FlightAware Γ£ê N67680 24-Jul-2024 (KFHR-KRNT) "</td><td>" sample\sample.kml "</td><td> 2024-07-24 23:19:04+00:00  </td><td> " barnabie point community center, Mercer Island "</td><td> 600.3937017000001 </td><td>  1299.1803556727484 </td><td> 425.39370170000007</td>
</tr>
<tr>
<td></td><td></td><td></td><td></td><td>" FlightAware Γ£ê N67680 24-Jul-2024 (KFHR-KRNT) "</td><td>" sample\sample.kml "</td><td> 2024-07-24 23:19:11+00:00  </td><td> " barnabie point community center, Mercer Island "</td><td> 549.6662781305727 </td><td>  442.6842478544879 </td><td>  374.66627813057266</td>
</tr>
<tr>
<td></td><td></td><td></td><td></td><td>" FlightAware Γ£ê N67680 24-Jul-2024 (KFHR-KRNT) "</td><td>" sample\sample.kml "</td><td> 2024-07-24 23:19:20+00:00  </td><td> " barnabie point community center, Mercer Island "</td><td> 498.6876648 </td><td>  1304.8682792190157 </td><td>  323.68766480000005</td>
</tr>
</tbody>
</table>

## Parameters

Parameters are:

<code>locationsfile target_kml output horizontal_feet altitude_feet</code>

#### Locations File Parameter

Path to file that lists the query locations for the search. If you wish to check all kml against proximity to a single location then the locations file will have a single entry. Format is specified below.

#### Target KML Parameter

This is path to a kml file, or path to a directory that will be searched for kml files to process.

#### Output parameter

Path to file where search will write results. Results are appended to this file in csv format. File will be created if it doesn't exist.

#### Horizontal Feet parameter (optional)

Optional parameter defaults to FAA distance of 2000ft. This is 'surface distance' and does not include altitude. Flight tracks that do not come within this distance of search location will not be reported.

#### Altitude Feet parameter (optional)

Optional parameter defaults to FAA 'congested region' location relative altitude of 1000ft. Flight tracks that are above search location by more than this distance will not be reported.

## Locations File Format

Location File contains the locations you are concerned about with each location on its own line.

Location file format is:

<pre><code>"location name", latitude, longitude, altitude in feet '</code></pre>

The source contains an example "searchlocations.txt" file that defines 3 search locations:

<pre><code>"beaux arts sailboat dock", 47.58407, -122.20493, 29
"beaux arts water tower, 10528 se 27th street, beaux arts", 47.586611, -122.199839, 300
"barnabie point community center, Mercer Island", 47.57695, -122.20374, 175</code></pre>

### How it works:

The plane flight tracks are not continuous, they are described as sets of points with an inferred LINE SEGMENT between them. This program searches each line segment for closest point on that line, then linearly interpolates time, altitude and location from the line segments two endpoints.

A better implementation would use a cubic spline to interpolate a curved path between points... but in samples I've seen airplanes are going fast, the sample rate is high enough that the curves are not significant.

In any case this is a tool to find potential violations, ultimately the FAA is the arbiter, send the data to them to decide.
