import pandas as pd
import numpy as np
import pycountry

df = pd.read_csv('../data/6-diff_flows.csv')
sfi = pd.read_csv('../data/assets/CSV-SFIv2018.csv')
p5 = pd.read_csv('../data/assets/CSV-p5v2018.csv')

# Combine unique values of party1&2
parties1 = list(df['ISO-Party1'].unique())
parties2 = list(df['ISO-Party2'].unique())

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
sfi_countries = list(sfi['ISO-country'].unique())
for sfi_country in sfi_countries:
    if sfi_country not in parties:
        problems.append(sfi_country)

# Extract data from sfi and place them in dataset

for index, rowDF in df.iterrows():
    year = rowDF['Year of signature']
    party1 = df.loc[index, 'ISO-Party1']
    party2 = df.loc[index, 'ISO-Party2']

    if (party1 not in parties or party2 not in parties):
        pass
    else:
        sfiP1 = sfi[ (sfi['ISO-country'] == party1) & (sfi['year'] == year) ]
        sfiP2 = sfi[ (sfi['ISO-country'] == party2) & (sfi['year'] == year) ]

        try:
            sfip1_v = -100 if sfiP1.empty else int(sfiP1['sfi'])
            sfip2_v = -100 if sfiP2.empty else int(sfiP2['sfi'])
        except TypeError as t:
            #yop[index] = sfiP1['country']
            #yop[index + 0.5] = sfiP2['country']
            #sfiP2['sfi'] = pd.to_numeric(sfiP2['sfi'])
            #print(sfiP2)
            print('Error:', sfiP1['country'])
            print('Error:', sfiP2['country'])

        maxSFI = max(sfip1_v, sfip2_v)
        maxSFI = maxSFI if maxSFI > -100 else None 
        df.loc[index, 'SFIP1'] = sfip1_v
        df.loc[index, 'SFIP2'] = sfip2_v
        df.loc[index, 'MaxSFI'] = maxSFI

# Extract data from demo and place them in dataset
for index, rowDF in df.iterrows():
    year = rowDF['Year of signature']
    party1 = df.loc[index, 'ISO-Party1']
    party2 = df.loc[index, 'ISO-Party2']

    if (party1 not in parties or party2 not in parties):
        pass
    else:
        p5P1 = p5[ (p5['ISO-country'] == party1) & (p5['year'] == year) ]
        p5P2 = p5[ (p5['ISO-country'] == party2) & (p5['year'] == year) ]

        try:
            p5p1_v = -100 if p5P1.empty else int(p5P1['democ'])
            p5p2_v = -100 if p5P2.empty else int(p5P2['democ'])
        except TypeError as t:
            #yop[index] = sfiP1['country']
            #yop[index + 0.5] = sfiP2['country']
            #sfiP2['sfi'] = pd.to_numeric(sfiP2['sfi'])
            #print(sfiP2)
            print('Error:', p5P1['country'])
            print('Error:', p5P2['country'])

        maxSFI = max(p5p1_v, p5p2_v)
        maxSFI = maxSFI if maxSFI > -100 else None 
        df.loc[index, 'democP1'] = p5p1_v
        df.loc[index, 'democP2'] = p5p2_v
        df.loc[index, 'MaxDemoc'] = maxSFI

# Rearrange columns order
cols_to_order = [
                'score', 'DiffFlowsTot', 'MaxGDPCurrent', 
                'MaxDemoc', 'democP1', 'democP2',
                'MaxSFI', 'SFIP1', 'SFIP2',
                'Party1', 'Party2', 'ISO-Party1', 'ISO-Party2',
                'Year of signature','name', 'Parties'
                ]
new_columns = cols_to_order + (df.columns.drop(cols_to_order).tolist())
df = df[new_columns]

# Export to csv
df.to_csv('../data/8-polity_vars_added.csv', index=False)
print('Done.')