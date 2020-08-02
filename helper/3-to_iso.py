import pandas as pd
import numpy as np
import pycountry

df = pd.read_csv('../data/2-scored.csv')

specials = {
    'Hong Kong, China SAR': 'HK',
    'Congo, Democratic Republic of the': 'CD',
    'EU (European Union)': 'EU',
    'Macao, China SAR': 'MO',
    'Niger': 'NG',
    'Kosovo': 'RKS'
}
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
        #Edge cases
        if country in specials:
            newName = specials[country]
        else:
            newName = country
    return newName

df['ISO-Party1'] = df['Party1'].apply(toISO)
df['ISO-Party2'] = df['Party2'].apply(toISO)

# Export to csv
df.to_csv('../data/3-iso.csv', index=False)
print('Done.')
