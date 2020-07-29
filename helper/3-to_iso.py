import pandas as pd
import numpy as np
import pycountry

df = pd.read_csv('../data/2-scored.csv')

# Transform Party1 and Party2 countries names into alpha-3 format for comfort
# https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
def toISO(country):
    country = str(country)
    try:
        newName = pycountry.countries.search_fuzzy(country)[0].alpha_3
    except LookupError:
        newName = country
    print(newName)
    return newName

df['ISO-Party1'] = df['Party1'].apply(toISO)
df['ISO-Party2'] = df['Party2'].apply(toISO)

# TODO
# Some edge cases:
'''
ASEAN - nan
BLEU - nan
Congo, Democratic Republic of the - CD (Congo, Dem. Rep.)
EFTA - nan
ERROR - nan
EU (European Union) - EU
Eurasian Economic Union - nan
Hong Kong, China SAR - HK (Hong Kong SAR, China)
Korea, Dem People's Rep of - nan
Macao, China SAR - MO (Macao SAR, China)
Taiwan Province of China - nan
'''


# Debug
print(df['ISO-Party1'].unique())
print(df['ISO-Party2'].unique())

# Export to csv
df.to_csv('../data/3-iso.csv', index=False)
print('Done.')
