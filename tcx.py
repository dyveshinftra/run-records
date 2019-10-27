#! /usr/bin/env python
import datetime
import os
import sys
import xml.etree.ElementTree as ET
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlwt import Workbook
from xlrd import open_workbook


class Record:
    def __init__(self, track_points):
        self.track_points = track_points

    def get_distance(self, idx):
        return float(
            self.track_points[idx].find("tcx:DistanceMeters", ns).text
        )

    def get_time(self, idx):
        return datetime.datetime.strptime(
            self.track_points[idx].find("tcx:Time", ns).text,
            "%Y-%m-%dT%H:%M:%S.000Z",
        )

    def distance(self, distance):
        begin_idx = 0
        end_idx = 0
        best_time_diff = 0.0
        while end_idx < len(self.track_points):
            distance_diff = self.get_distance(end_idx) - self.get_distance(
                begin_idx
            )
            if distance_diff < distance:
                end_idx += 1
                if end_idx < len(self.track_points):
                    distance_diff2 = self.get_distance(end_idx) - self.get_distance(
                        begin_idx
                    )
                    if distance_diff2 > distance:
                        time_diff = (
                            (self.get_time(end_idx - 1) - self.get_time(begin_idx)).seconds
                            * distance
                        ) / distance_diff
                        if not best_time_diff or time_diff < best_time_diff:
                            best_time_diff = time_diff
            else:
                time_diff = (
                    (self.get_time(end_idx) - self.get_time(begin_idx)).seconds
                    * distance
                ) / distance_diff
                if not best_time_diff or time_diff < best_time_diff:
                    best_time_diff = time_diff
                begin_idx += 1
        if not best_time_diff:
            return best_time_diff
        s, ms = divmod(best_time_diff, 1)
        s = int(s)
        ms = int(ms * 1000000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return str(datetime.time(h, m, s, ms))


try:
    entries = os.listdir(sys.argv[1])
    for tcx_file in entries:
        tcx_file = os.path.join(sys.argv[1], tcx_file)
except NotADirectoryError:
    # for Python3
    entries = [os.path.join(".", sys.argv[1])]
records = {}
r_wb = open_workbook("records.xls")
wb = copy(r_wb)
# add_sheet is used to create sheet.
r_sheet1 = r_wb.sheet_by_index(0)
sheet1 = wb.get_sheet(0)
file_number = -1
distances = [
    100,
    200,
    400,
    800,
    1000,
    1500,
    1609.344,
    2000,
    3000,
    5000,
    10000,
    20000,
]
for tcx_file in entries:
    if os.path.isfile(tcx_file) and tcx_file.endswith(".tcx"):
        file_number += 1
        tcx_file = ET.parse(tcx_file)
        root = tcx_file.getroot()
        ns = {
            "tcx": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
        }
        # check all activities for any running activity
        for activity in root.findall("tcx:Activities/tcx:Activity", ns):
            record_id = activity.findall("tcx:Id", ns)[0].text
            if record_id == r_sheet1.row(0)[file_number + 3].value:
                continue
            if activity.get("Sport") == "Running":
                record = Record(
                    activity.findall("tcx:Lap/tcx:Track/tcx:Trackpoint", ns)
                )
                sheet1.write(0, file_number + 3, record_id)
                for i, x in enumerate(distances):
                    new_record = record.distance(x)
                    if new_record and (x not in records or records.get(x) > new_record):
                        records[x] = new_record 
                    sheet1.write(i + 1, file_number + 3, new_record)

sheet1.write(0, 1, "records")

for i in range(len(distances)):
    distance = str(distances[i])
    total_record = records.get(distances[i])
    # sheet1.write(i + 1, 0, str(distances[i]))
    r_value = r_sheet1.row(i + 1)[1].value
    if (total_record and (r_value == "-" or total_record < r_value)):
        sheet1.write(i + 1, 1, total_record or "-")
        print(f"{distance}:    \t{total_record}")
    elif r_value != "-":
        print(f"{distance}:    \t{r_value}")
    else:
        print(f"{distance}:    \t-")

wb.save("records.xls")
