import pandas as pd
import numpy as np
import pycountry

df = pd.read_csv('../data/6-diff_flows.csv')
sfi = pd.read_excel('../data/assets/SFIv2018.xls')

# Combine unique values of party1&2
parties1 = list(df['Party1'].unique())
parties2 = list(df['Party2'].unique())

'''
Some countries or regions (like the ASEAN) have no Polity equivalent
'''
not_in_wb = set(['ASEAN (Association of South-East Asian Nations)', 'BLEU (Belgium-Luxembourg Economic Union)',
'EFTA (European Free Trade Association)', 'ERROR', 'Sudan',
'Eurasian Economic Union', "Korea, Dem People's Rep of", 'COK', 'PSE', 'EU'
])
parties = list( (set(parties1) | set(parties2)) - not_in_wb)
parties = sorted(parties)

# Check if some countries are not the same in the 2 datasets
problems = []
sfi_countries = list(sfi['country'].unique())
for sfi_country in sfi_countries:
    if sfi_country not in parties:
        problems.append(sfi_country)
'''
['Belgium', 'Bhutan', 'Bolivia', 'Cape Verde', 'Congo-Brazzaville', 'Czech Republic', 'Timor Leste', 'Fiji', 'Iran', "Cote d'Ivoire", 
'Kosovo', 'Laos', 'Luxembourg', 'Macedonia', 'Moldova', 'Korea, North', 'Korea, South', 'Russia', 'Sudan (North)', 'Slovak Republic', 
'Solomon Islands', 'South Sudan', 'Swaziland', 'Syria', 'Taiwan', 'Tanzania', 'United States', 'Venezuela', 'Vietnam', 'Serbia & Montenegro', 
'Dem. Rep. of Congo']
'''
# Translate country names from polity's dataset to original dataset
# could have converted polity's to ISO.....................
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

# Extract data from sfi and place them in dataset
for index, rowDF in df.iterrows():
    year = rowDF['Year of signature']
    party1 = df.loc[index, 'Party1']
    party2 = df.loc[index, 'Party2']

    if (party1 not in parties or party2 not in parties):
        pass
    else:
        # Convert country names 
        if party1 in equivalent_data.values():
            party1 = equivalent_data[list(equivalent_data.values).index(party1)]
        elif party2 in equivalent_data.values():
            party2 = equivalent_data[list(equivalent_data.values).index(party2)]
        
        sfiP1 = sfi[ (sfi['country'] == party1) & (sfi['year'] == year) ]
        sfiP2 = sfi[ (sfi['country'] == party2) & (sfi['year'] == year) ]

        #df.loc[index, 'SFIP1'] = 1
        #df.loc[index, 'SFIP2'] = 2
        #df.loc[index, 'MaxSFI'] = maxSFI
        
        print(party1, sfiP1['sfi'])
        print(party2, sfiP2['sfi'])
        '''
        if sfiP2.empty:
            maxSFI = sfiP1['sfi']
            print(maxSFI, type(maxSFI))
        elif sfiP1.empty:
            maxSFI = sfiP2['sfi']
            print(maxSFI, type(maxSFI))
        else:
            maxSFI = sfiP1['sfi'] if sfiP1['sfi'] > sfiP2['sfi'] else sfiP2['sfi']
            print(maxSFI, type(maxSFI))
        '''


# Rearrange columns order
cols_to_order = [
                'score', 'DiffFlowsTot', 'MaxGDPCurrent', 
                'Party1', 'Party2', 'ISO-Party1', 'ISO-Party2',
                'Year of signature','name', 'Parties'
                ]
new_columns = cols_to_order + (df.columns.drop(cols_to_order).tolist())
df = df[new_columns]

# Export to csv
df.to_csv('../data/7-polity_vars_added.csv', index=False)
print('Done.')