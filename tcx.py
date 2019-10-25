#! /usr/bin/env python

import datetime
import sys
import xml.etree.ElementTree as ET

from Tkinter import *

tcx_file = ET.parse(sys.argv[1])
root = tcx_file.getroot()
ns = { 'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2', }

class Record:
	def __init__(self, track_points):
		self.track_points = track_points
	def get_distance(self, idx):
		return float(self.track_points[idx].find('tcx:DistanceMeters', ns).text)
	def get_time(self, idx):
		return datetime.datetime.strptime(self.track_points[idx].find('tcx:Time', ns).text, '%Y-%m-%dT%H:%M:%S.000Z')
	def distance(self, distance):
		begin_idx = 0
		end_idx = 0
		best_time_diff = 0.0
		while end_idx < len(self.track_points):
			distance_diff = self.get_distance(end_idx) - self.get_distance(begin_idx)
			if distance_diff < distance:
				end_idx += 1
			else:
				time_diff = ((self.get_time(end_idx) - self.get_time(begin_idx)).seconds * distance) / distance_diff
				if not best_time_diff or time_diff < best_time_diff:
					best_time_diff = time_diff
				begin_idx += 1
		s, ms = divmod(best_time_diff, 1)
		s = int(s)
		ms = int(ms*1000000)
		m, s = divmod(s, 60)
		h, m = divmod(m, 60)
		return str(datetime.time(h, m, s, ms))

# check all activities for any running activity
for activity in root.findall('tcx:Activities/tcx:Activity', ns):
	if activity.get('Sport') == 'Running':
		record = Record(activity.findall('tcx:Lap/tcx:Track/tcx:Trackpoint', ns))
		distances = [100, 200, 400, 800, 1000, 1500, 1609.344, 2000, 3000, 5000, 10000, 20000]
		records = map(lambda x: record.distance(x), distances)

		root = Tk()
		for i in range(len(distances)):
			b1 = Entry(root)
			b1.grid(row=i, column=0)
			b1.insert(0, str(distances[i]))

			b2 = Entry(root)
			b2.grid(row=i, column=1)
			b2.insert(0, records[i])
		mainloop()
