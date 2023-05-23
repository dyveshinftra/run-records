"""
Export Komoot tour/route when region is locked.

How to find second link from first?
https://www.komoot.com/tour/1130340804/edit
https://www.komoot.com/api/routing/tour?query=d06Av_adgBDAaM%3DFxhcBIBzvpMIxK_tQPCpsAIIqVQ27IEewVkKe8OXGICSwWBOHTDg3IVrCsTPd-RlJJH9QSoRSGD7KiZDGxc5EV8krCp-hSIjhJWAr9UuECySsDl3JkMkTveVviM2-bJ3jGIGC7oxP8zQTGPrHg0JPgKfeefa0geBTvGQQ0dUXGeiseoqfe8-D-A%3D&_embedded=coordinates%2Cway_types%2Csurfaces%2Cdirections
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
