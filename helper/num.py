import pandas as pd
import re

treaties = pd.read_csv('./data/data.csv')

# Let's delete some useless data
del treaties['Treaty full text']
del treaties['IIA content']
del treaties['Mapped by']
del treaties['About']
del treaties['Short title:']
del treaties['Treaty investment chapter text']

# Strip 'Parties' column of \r\n
treaties['Parties'] = treaties['Parties'].replace('\\r\\n', ' ', regex = True) 

def get_parties(parties):
    party = re.split(r'\d', parties)

    # First item of list is empty, delete it
    del party[0]

    # Some cleaning
    party = [p.replace('.', '') for p in party]
    party = [p.strip(' ') for p in party]
    
    # If there is one party missing, let's catch the error
    try:
        party1 = party[0]
        party2 = party[1]
    except IndexError:
        party2 = 'ERROR'
    
    return party1, party2

# Extract the different parties
treaties['Party1'] = treaties['Parties'].map(lambda x: get_parties(x)[0])
treaties['Party2'] = treaties['Parties'].map(lambda x: get_parties(x)[1])

# Rearrange column names
cols = ['Party1', 'Party2'] + [col for col in treaties if col != 'Party1' and col != 'Party2']
treaties = treaties[cols]

# Rearrange dataframe index
treaties.index = [x for x in range(1, len(treaties.values)+1)]
treaties.index.name = 'id'

# Check if it seems ok
print(treaties['Party1'].describe())
print(treaties['Party2'].describe())
print(treaties.describe())

# Export dataframe into new csv
treaties.to_csv('./data/data_cleaned.csv')
