"""Strava to GPX Converter

Strava activity data is fetched from this URL:
    https://www.strava.com/activities/<ID>/streams?stream_types[]=latlng"""

import json
import xml.etree.ElementTree as ET

gpx = ET.Element('gpx', {'version':'1.1', 'creator':'divvy', 'xmlns':'http://www.topografix.com/GPX/1/1'})
trk = ET.SubElement(gpx, 'trk')
trkseg = ET.SubElement(trk, 'trkseg')

for lat, lon in json.load(open('streams.json'))['latlng']:
    ET.SubElement(trkseg, 'trkpt', {'lat':str(lat),' lon':str(lon)})

open('streams.gpx', 'w').write(ET.tostring(gpx, encoding="unicode"))
