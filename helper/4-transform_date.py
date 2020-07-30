import pandas as pd
import re

df = pd.read_csv('../data/3-iso.csv')

# Transform 'Date of signature' column into 'Year of signature' by extracting year with Regex
# and rename column into 'Year of signature'
def transformDate(field):
    m = re.search(r'(\d{4})', str(field))
    if m:
        year = m.group(1)
    return year
df['Year of signature'] = df['Date of signature'].apply(transformDate)
del df['Date of signature']

# Some problems with data older than 1960, delete them
df.drop(df[df['Year of signature'].map(int) < 1960].index, inplace=True)

# Rearrange columns order
cols_to_order = [
                'score', 'Party1', 'Party2', 'ISO-Party1', 'ISO-Party2',
                'Year of signature','name', 'Parties'
                ]
new_columns = cols_to_order + (df.columns.drop(cols_to_order).tolist())
df = df[new_columns]

# Export to csv
df.to_csv('../data/4-date_transformed.csv', index=False)
print('Done.')