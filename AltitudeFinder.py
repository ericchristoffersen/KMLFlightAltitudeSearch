
from fastkml import kml
from fastkml import geometry
from fastkml import gx
import datetime
import sys
import geopy.distance
from itertools import cycle

from shapely.geometry import LineString, Point
import numpy as np

import sys

def m2ft(m) :
    return m * 3.2808399

def ft2m(ft) :
    return ft / 3.2808399

def ft2km(ft) :
    return ft / 3280

from datetime import datetime, timedelta

def round_timedelta(td):
    return timedelta(seconds=int(td.total_seconds()))

def closestPointOnSegment(p1, p2, p3):

    A = np.array([p1[0], p1[1], p1[2]])
    B = np.array([p2[0], p2[1], p2[2]])
    C = np.array([p3[0], p3[1], p3[2]])
    
    line_segment = LineString([A, B])
    
    norm = np.linalg.norm(B - A)

    if norm == 0:
        return A, 0
    
    d = np.linalg.norm(np.cross(B - A, C - A)) / np.linalg.norm(B - A)
    
    n = B - A
    v = C - A
    t = np.dot(v, n) / np.dot(n, n)
    t = max(0, min(1, t))
    Z = A + t * n
    
    return [[Z[0], Z[1], Z[2]], t]

def print_child_features(element, outFile, depth=0 ):
    """Prints the name of every child node of the given element, recursively."""
    if not getattr(element, "features", None):
        return
    for feature in element.features:
        print("  " * depth + feature.name, file=outFile)
        print_child_features(feature, outFile, depth + 1)

def get_child_top_feature_name(element):
    if not getattr(element, "features", None):
        return ""
    for feature in element.features:
        return feature.name

import xml.etree.ElementTree as ET
import datetime
from collections import namedtuple

import math

Position = namedtuple("Position", ["dt", "longitude", "latitude", "altitude"])

Loc = namedtuple("Loc", ["name", "latitude", "longitude", "altitude"])


def read_kml_track(fname):
    tree = ET.parse(fname)
    root = tree.getroot()
    ns = {
        "kmlns": "http://www.opengis.net/kml/2.2",
        "gx": "http://www.google.com/kml/ext/2.2",
    }
    # track_elements = root.find("kmlns:Placemark/gx:Track", namespaces=ns)
    track_elements = root.find("kmlns:Document/kmlns:Placemark/gx:Track", namespaces=ns)
    lst_when = track_elements.findall("kmlns:when", namespaces=ns)
    lst_coord = track_elements.findall("gx:coord", namespaces=ns)
    for when, coord in zip(lst_when, lst_coord):
        dt = datetime.datetime.strptime(when.text, "%Y-%m-%dT%H:%M:%S%z")

        #dt = datetime.datetime(dt.year,dt.month, dt.day, dt.hour, dt.minute, dt.second);
        s = coord.text
        longitude, latitude, altitude = s.replace(",", ".").split()
        longitude, latitude, altitude = map(float, (longitude, latitude, altitude))
        yield Position(dt, longitude, latitude, altitude)

import pymap3d as pm

def checkLoc(kmltag, inpath, outFile, p, nextp, minAlt, minDist, loc) :
    latlon = Loc("on route", p.latitude, p.longitude, p.altitude)    
    pPair = (latlon.latitude, latlon.longitude)
    locPair = (loc.latitude, loc.longitude)
    nextpPair = (nextp.latitude, nextp.longitude)

    x0, y0, z0 = pm.geodetic2ecef(loc.latitude, loc.longitude, 0)
    x1, y1, z1 = pm.geodetic2ecef(p.latitude, p.longitude, 0)
    x2, y2, z2 = pm.geodetic2ecef(nextp.latitude, nextp.longitude, 0)

    r = closestPointOnSegment([x1,y1,z1],[x2,y2,z2],[x0,y0,z0])
    closestP = r[0]
    t = r[1]
    closestLLA = pm.ecef2geodetic(closestP[0], closestP[1], closestP[2])
    coords_closest = (closestLLA[0], closestLLA[1])
    alt_closest = p.altitude + (nextp.altitude - p.altitude) * t
    closestTime = p.dt + round_timedelta((nextp.dt - p.dt) * t)

    distkmP = geopy.distance.geodesic(locPair, pPair).km
    distkmNextP = geopy.distance.geodesic(locPair, nextpPair).km
    distkmClosest = geopy.distance.geodesic(locPair, coords_closest).km

    if alt_closest < (minAlt + loc.altitude) and distkmClosest < minDist:
        print(",",",",",",",","\"",kmltag, "\", \"", inpath, "\"," , closestTime, " , \"", loc.name, "\",", m2ft(alt_closest), ", ", m2ft(distkmClosest* 1000), ", ", m2ft(alt_closest - loc.altitude), file=outFile)

def readAndReport(filenames, outFileName, minAlt, minDist, locList):

    with open(outFileName, 'a', encoding="utf-8") as outFile :

        for fname in filenames:

            with open(fname, encoding="utf-8") as kml_file:
                k = kml.KML.class_from_string(kml_file.read().encode("utf-8"), strict=False)
        
                if False:
                    for feature0 in k.features:
                        #print("{}, {}".format(feature0.name, feature0.description))
                        for feature1 in feature0.features:
                            if isinstance(feature1.geometry, geometry.Point):
                                point = feature1.geometry
                                print(point)
            
                            if isinstance(feature1, gx.Track):
                                for track in feature1.tracks:
                                    
                                    running = True
                                    licycle = cycle(track)
                                    nextpos = next(licycle)
                                    while running:
                                        position, nextpos = nextpos, next(licycle)
                                        dt = datetime.datetime.strptime(position['when'], "%Y-%m-%dT%H:%M:%S%z")
                                        longitude, latitude, altitude = map(float, position['coord'].split(','))
                                        print( dt, longitude, latitude, altitude)
        
                kmltag = get_child_top_feature_name(k)

                print(kmltag, " file:", fname);
                
                positions = read_kml_track(fname)
    
                running = True
                licycle = cycle(positions)
                nextp = next(licycle)
                bigtimep = nextp
                while running:
                    p, nextp = nextp, next(licycle)
                
                    for l in locList:
                        checkLoc(kmltag, fname, outFile, p, nextp, minAlt, minDist, l)
                    if p.dt >= nextp.dt:
                        break
                    
import os
from os import listdir
from os.path import isfile, join

import csv
from io import StringIO

if __name__ == "__main__":

    argCount = len(sys.argv)
    if argCount < 4:
        print("Error: must provide locationfile, path to target file(s), and path to append file")

    locationPath = sys.argv[1]
    sourcePath = sys.argv[2]
    appendFile = sys.argv[3]
    
    distanceCriteria = 0.5 #km, 0.5 is 1640.4ft.
    altitudeCriteria = 304.8 #meters is 1000ft
    if argCount > 4:
        distanceCriteria = ft2km(float(sys.argv[4]))
        
    if argCount > 5:
        altitudeCriteria = ft2m(float(sys.argv[5]))

    locs = []
    with open(locationPath, 'r', encoding="utf-8") as location_file:
        locationLines = location_file.readlines()
        for lines in locationLines:
            data = StringIO(lines)
            reader = csv.reader(data, delimiter=',')            
            for row in reader:
                locationName = row[0]
                lat = float(row[1])
                lon = float(row[2])
                alt = ft2m(float(row[3]))
            
                locs.append(Loc(locationName, lat, lon, alt))

    if len(locs) > 0:
        with open(appendFile, 'a') as outFile :
            print("search location name, location lat, location lon, location alt (ft), kmltag, filename, time, location name, reported altitude (ft), distance (ft), altitude above location(ft)", file=outFile)
            for l in locs:
                print("\"", l.name, "\",", l.latitude,",", l.longitude,",", m2ft(l.altitude), file=outFile)
    else:
        print("Error: Locations must be provided in location file.")
        quit()

    files = [sourcePath]
    if os.path.isdir(sourcePath) :
        files = []
        for f in listdir(sourcePath):
            fpath = join(sourcePath, f)
            if isfile(fpath):
                if fpath.endswith(".kml"):
                    files.append(fpath)
    
    readAndReport(files, appendFile, altitudeCriteria, distanceCriteria, locs)