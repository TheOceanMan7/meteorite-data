#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import datetime
import regex as re


def extract_year(iso_timestamp):
    return datetime.datetime.strptime(iso_timestamp, '%Y-%m-%dT%H:%M:%S.%f').year

def meteorite_genclassifier(meteorite_recclass):

    if re.search(r'Lunar', meteorite_recclass, re.I):
        return 'MOON'

    elif re.search(r'Martian', meteorite_recclass, re.I):
        return 'MARS'

    elif re.search(r'O?C[0-9]?[A-Z]?', meteorite_recclass, re.I) \
        or re.search(r'\b[EHKLR][LH]?[0-9]?\b', meteorite_recclass, re.I) \
        or re.search(r'(?<!Pallas|Mesosider)ite', meteorite_recclass, re.I) \
        or re.search(r'Stone-ung', meteorite_recclass, re.I):
        return 'STONE'

    elif re.search(r'(Pallas|Mesosider)ite', meteorite_recclass, re.I):
        return 'STONY_IRON'

    elif re.search(r'Iron', meteorite_recclass, re.I):
        return 'IRON'

    else:
        return 'OTHER'

def price_tagger(meteorite_genclass):

    if meteorite_genclass['genclass'] in 'MOON' or meteorite_genclass['genclass'] in 'MARS':
        return meteorite_genclass['mass'] * 1000.0

    elif meteorite_genclass['genclass'] in 'STONE':
        return meteorite_genclass['mass'] * 20.0

    elif meteorite_genclass['genclass'] in 'STONY_IRON':
        return meteorite_genclass['mass'] * 12.0

    elif meteorite_genclass['genclass'] in 'IRON':
        return meteorite_genclass['mass'] * 5.0

    else:
        return meteorite_genclass['mass'] * 0.5

url = 'https://data.nasa.gov/resource/gh4g-9sfh.csv'
df = pd.read_csv(url)

#Grab data from meteorites fallen to Earth
fallen = df[df['fall'] == 'Fell']


clean_fallen = fallen.dropna(how='any', axis=0)
clean_fallen = clean_fallen.drop(columns='geolocation')
clean_fallen = clean_fallen[(clean_fallen['reclat'] != 0.0) & (clean_fallen['reclong'] != 0.0)]
clean_fallen = clean_fallen[(clean_fallen.nametype != 'Relict')]
clean_fallen['year'] = clean_fallen['year'].apply(extract_year)
clean_fallen = clean_fallen[(clean_fallen.year <= 2022)]
clean_fallen = clean_fallen.drop(columns='nametype')
clean_fallen = clean_fallen.drop(columns='fall')
clean_fallen['genclass'] = clean_fallen['recclass'].apply(meteorite_genclassifier)
clean_fallen['price'] = clean_fallen.apply(price_tagger, axis=1)
