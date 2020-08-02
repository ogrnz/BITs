import pandas as pd
import numpy as np
import pycountry

print('Running...')

#sfi = pd.read_excel('../data/assets/SFIv2018.xls')
p5 = pd.read_excel('../data/assets/p5v2018.xls')
sfi = p5

# Delete entries if year < 1960 
sfi.drop(sfi[sfi['year'].map(int) < 1960].index, inplace=True)

equivalent_data = {
    'Bolivia': 'Bolivia, Plurinational State of',
    'Cape Verde': 'Cabo Verde',
    'Congo-Brazzaville': 'Congo',
    'Dem. Rep. of Congo': 'Congo, Democratic Republic of the',
    'Czech Republic': 'Czechia',
    'Timor Leste': 'Timor-Leste',
    "Cote d'Ivoire": "Côte d'Ivoire",
    'Macedonia': 'North Macedonia',
    'Moldova': 'Moldova, Republic of',
    'Korea, South': 'Korea, Republic of',
    'Russia': 'Russian Federation',
    'Slovak Republic': 'Slovakia',
    'Syria': 'Syrian Arab Republic',
    'Taiwan': 'Taiwan Province of China',
    'Tanzania': 'Tanzania, United Republic of',
    'United States': 'United States of America',
    'Venezuela': 'Venezuela, Bolivarian Republic of',
    'Vietnam': 'Viet Nam'
}
specials = {
    'Cape Verde': 'CPV',
    'Congo-Brazzaville': 'COG',
    'Dem. Rep. of Congo': 'COD',
    'Czech Republic': 'CZE',
    'Timor Leste': 'TLS',
    "Cote d'Ivoire": "CIV",
    'Macedonia': 'MKD',
    'Moldova': 'MDA',
    'Niger': 'NG',
    'Korea, South': 'KOR',
    'Kosovo': 'RKS',
    'Russia': 'RUS',
    'Slovak Republic': 'SVK',
    'Syria': 'SYR',
    'Taiwan': 'Taiwan Province of China',
    'Tanzania': 'TZA',
    'United States': 'USA',
    'Venezuela': 'VEN',
    'Vietnam': 'VNM'
}
not_in_db = ['Serbia & Montenegro', 'Swaziland', 'Sudan (North)', 'Korea, North', 'Laos']

# Transform Party1 and Party2 countries names into alpha-3 format for comfort
# https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
def toISO(country):
    country = str(country)
    try:
        if country in specials:
            newName = specials[country]
        else:
            newName = pycountry.countries.search_fuzzy(country)[0].alpha_3
    except LookupError:
        if country in specials:
            newName = specials[country]
        elif country in not_in_db:
            return country
        else:
            return country
    return newName

sfi['ISO-country'] = sfi['country'].apply(toISO)

# Export to csv
#sfi.to_csv('../data/assets/CSV-SFIv2018.csv', index=False)
p5 = sfi
p5.to_csv('../data/assets/CSV-p5v2018.csv', index=False)
print('Done.')