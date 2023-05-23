"""
Export Komoot tour/route when region is locked.

The tour/route must be planned in your account!

Steps to follow:
1.  Go to tour/route e.g.: https://www.komoot.com/nl-nl/tour/1130340804
2.  View source and search for query\":\" to find the query ID
3.  Save query https://www.komoot.com/api/routing/tour?query=<QUERY D>&_embedded=coordinates%2Cway_types%2Csurfaces%2Cdirections
"""

import json
import xml.etree.ElementTree as ET

gpx = ET.Element('gpx', {'version':'1.1', 'creator':'divvy', 'xmlns':'http://www.topografix.com/GPX/1/1'})
trk = ET.SubElement(gpx, 'trk')
trkseg = ET.SubElement(trk, 'trkseg')

for item in json.load(open('tour.json'))['_embedded']['coordinates']['items']:
    lat = item['lat']
    lng = item['lng']
    ET.SubElement(trkseg, 'trkpt', {'lat':str(lat),' lon':str(lng)})

open('streams.gpx', 'w').write(ET.tostring(gpx, encoding="unicode"))
