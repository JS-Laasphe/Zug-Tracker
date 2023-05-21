# Dokumentiert die eventuelle Verspätung ankommender Züge eines Bahnhofs.
# In den Pyhafas-Einstellungen kann festgelegt werden, welche Zuggattungen getrackt werden sollen.
# Die Daten werden in einer CSV-Datei gespeichert, welche zur Nachbearbeitung von Filter.py benutzt wird.

import csv
import datetime
from typing import List
from pyhafas import HafasClient
from pyhafas.profile import DBProfile
from pyhafas.types.fptf import Leg
import os.path

# Pyhafas-Einstellungen
client = HafasClient(DBProfile())
locations = client.locations("Marburg(Lahn)")
best_found_location = locations[0]

arrivals: List[Leg] = client.arrivals(
    station=best_found_location.id,
    date=datetime.datetime.now(),
    max_trips=4,
    products={
        "long_distance_express": True,
        "regional_express": True,
        "regional": True,
        "suburban": False,
        "bus": False,
        "ferry": False,
        "subway": False,
        "tram": False,
        "taxi": False
    }
)

# Einstellungen/Inhalt der CSV-Datei
header = ["Name", "Herkunft", "Ankunft", "Verspätung", "Ausgefallen"]

rows = []
for leg in arrivals:
    leg_data = leg.__dict__

    name = leg_data["name"]
    direction = leg_data["direction"]
    dateTime = leg_data["dateTime"].strftime("%Y-%m-%d %H:%M:%S")
    cancelled = leg_data["cancelled"]
    delay = leg_data["delay"]

    row = [name, direction, dateTime, delay, cancelled]
    rows.append(row)

filename = "unfiltered.csv"
file_exists = os.path.isfile(filename)

with open(filename, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    if not file_exists or file.tell() == 0:
        writer.writerow(header)
    writer.writerows(rows)
