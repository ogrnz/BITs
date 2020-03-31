import pandas as pd

treaties = pd.read_csv('../data/data.csv')

# Let's delete some useless data
del treaties['Treaty full text']
del treaties['IIA content']
del treaties['Mapped by']
del treaties['About']
del treaties['Short title:']
del treaties['Treaty investment chapter text']

# Strip 'Parties' column of \r\n
treaties['Parties'] = treaties['Parties'].replace('\\r\\n', ' ', regex = True) 

# Export df into new csv
treaties.to_csv('../data/data_cleaned.csv')