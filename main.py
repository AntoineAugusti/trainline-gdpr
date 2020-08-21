#!/usr/bin/env python
import json
from argparse import ArgumentParser
from collections import defaultdict

import pandas as pd
import numpy as np
from haversine import haversine

parser = ArgumentParser()
parser.add_argument('filepath', help='The full path to the Trainline JSON file')
parser.add_argument('--first-name', help='Filter journeys with a specific traveler first name')
args = parser.parse_args()

with open(args.filepath) as f:
    data = json.load(f)

res = defaultdict(list)
totals = defaultdict(int)
for pnr in data['pnrs']:
    travelers_first_names = [t["first_name"] for t in pnr["travelers"]]
    if (
        pnr['status'] == 'emitted' and not pnr['cancelled'] and
        (args.first_name is None or args.first_name in travelers_first_names)
    ):
        if pnr.get("price"):
            totals["price"] += pnr["price"]["cents"]
            totals["price_per_traveler"] += float(pnr["price"]["cents"]) / len(pnr["travelers"])
        for leg in pnr['legs']:
            res['code'].append(pnr['code'])
            res['booked_at'].append(pnr['booked_at'])

            res['carrier'].append(leg['carrier'])
            res['travel_class'].append(leg['travel_class'])
            res['train_type'].append(leg['train']['type'])
            res['train_number'].append(leg['train']['number'])
            res['departure_date'].append(leg['departure_date'])
            res['arrival_date'].append(leg['arrival_date'])
            res['co2_emission'].append(leg['co2_emission'])

            for direction in ['departure', 'arrival']:
                for key in ['slug', 'latitude', 'longitude', 'name', 'country', 'public_id']:
                    res[direction + '_' + key].append(leg[direction][key])


df = pd.DataFrame(res, columns=res.keys())
grouped = df.groupby(['departure_slug', 'arrival_slug']).size().rename('total_travel_for_leg')
df = df.join(grouped, on=['departure_slug', 'arrival_slug'])
df['distance_km'] = np.round(
    haversine(
        df.departure_latitude, df.departure_longitude,
        df.arrival_latitude, df.arrival_longitude
    ),
    2
)
df.to_csv('data.csv', index=False)

print("total price: %s EUR" % round(float(totals["price"]) / 100))
print("total price per traveler: %s EUR" % round(float(totals["price_per_traveler"]) / 100))
print("total distance: %s km" % round(np.sum(df.distance_km)))
print(
    "average price/km/traveler : %s EUR/km/passenger" %
    round(float(totals["price_per_traveler"]) / 100.0 / np.sum(df.distance_km), 2)
)
