import pandas as pd
import re
from pandas_datareader import wb

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

# Describe values
#print(df['Year of signature'].describe())
#print(df['Year of signature'].max()) #2018
#print(df['Year of signature'].min()) #1959

# Test with restricted dataset
#df = df[0:3]

# FDI outflows Worldbank indicator:
# BM.KLT.DINV.WD.GD.ZS

# FDI inflows indicator:
# BX.KLT.DINV.WD.GD.ZS

# Combine unique values of party1&2
parties1 = list(df['ISO-Party1'].unique())
parties2 = list(df['ISO-Party2'].unique())
parties = list(set(parties1) | set(parties2))

# Download indicators data
WBdata = wb.download(indicator=['BM.KLT.DINV.WD.GD.ZS', 'BX.KLT.DINV.WD.GD.ZS'], country=parties, errors="raise", start=1900, end=2019)

'''
ValueError from WB:
ASEAN (Association of South-East Asian Nations), BLEU (Belgium-Luxembourg Economic Union), 
Congo, Democratic Republic of the, EFTA (European Free Trade Association), ERROR, EU (European Union), 
Eurasian Economic Union, Hong Kong, China SAR, Korea, Dem People's Rep of, Macao, China SAR, Taiwan Province of China

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

for index, rowDF in df.iterrows():
    party1 = rowDF['Party1']
    year = rowDF['Year of signature']

    df.loc[index, 'FDIOutflowsP1'] = WBdata.loc[party1, year][0]
    df.loc[index, 'FDIInflowsP1'] = WBdata.loc[party1, year][1]

# Rearrange columns order
cols_to_order = ['score', 'Party1', 'Party2', 'ISO-Party1', 'ISO-Party2','Year of signature','name', 'Parties']
new_columns = cols_to_order + (df.columns.drop(cols_to_order).tolist())
df = df[new_columns]

# Export to csv
df.to_csv('../data/4-added_variables.csv', index=False)
print('Done.')
