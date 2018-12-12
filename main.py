#!/usr/bin/env python
import json
from argparse import ArgumentParser
from collections import defaultdict

import pandas as pd

parser = ArgumentParser()
parser.add_argument('filepath', help='The full path to the Trainline JSON file')
args = parser.parse_args()

with open(args.filepath) as f:
    data = json.load(f)

res = defaultdict(list)
for pnr in data['pnrs']:
    if pnr['status'] == 'emitted' and not pnr['cancelled']:
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
df.to_csv('data.csv', index=False)
