import pandas as pd
import numpy as np
from pandas_datareader import wb
import pycountry

df = pd.read_csv('../data/4-date_transformed.csv')

# Combine unique values of party1&2
parties1 = list(df['ISO-Party1'].unique())
parties2 = list(df['ISO-Party2'].unique())

'''
Some countries or regions (like the ASEAN) have no Worldbank equivalent
or no data available altogether and thus raise a ValueError when contacting
the API so we remove them from our parties list
'''
not_in_wb = set(['ASEAN (Association of South-East Asian Nations)', 'BLEU (Belgium-Luxembourg Economic Union)',
'EFTA (European Free Trade Association)', 'ERROR',
'Eurasian Economic Union', "Korea, Dem People's Rep of",
'Taiwan Province of China', 'COK', 'PSE'
])
parties = list( (set(parties1) | set(parties2)) - not_in_wb)
parties = sorted(parties)

# EU not in hardcoded Worldbank country list
# Hotfix
wb.country_codes.append('EU')

'''
Download Worldbank indicators data
FDI outflows:
BM.KLT.DINV.WD.GD.ZS
FDI inflows:
BX.KLT.DINV.WD.GD.ZS
'''
WBdata = wb.download(indicator=['BM.KLT.DINV.WD.GD.ZS', 'BX.KLT.DINV.WD.GD.ZS'], country=parties, errors='raise', start=1900, end=2019)

# Convert WBdata countries into ISO
# https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
# so we can rename WBdata index
def toISO(country):
    country = str(country)
    try:
        newName = pycountry.countries.search_fuzzy(country)[0].alpha_3
    except LookupError:
        newName = country
    return newName

'''
# Script used to generate the dict
converted_dict = {}
for i, row in WBdata.iterrows():
    print(i[0])
    if i[0] in converted_dict:
        pass
    else:
        converted_dict[i[0]] = str(toISO(i[0]))
'''

# We cache the converted_dict
converted_dict = {'Afghanistan': 'AFG', 'Angola': 'AGO', 'Albania': 'ALB', 'United Arab Emirates': 'ARE', 'Argentina': 'ARG', 'Armenia': 'ARM', 'Antigua and Barbuda': 'ATG', 'Australia': 'AUS', 'Austria': 'AUT', 'Azerbaijan': 'AZE', 'Burundi': 'BDI', 'Benin': 'BEN', 'Burkina Faso': 'BFA', 
'Bangladesh': 'BGD', 'Bulgaria': 'BGR', 'Bahrain': 'BHR', 'Bosnia and Herzegovina': 'BIH', 'Belarus': 'BLR', 'Belize': 'BLZ', 'Bolivia': 'BOL', 'Brazil': 'BRA', 'Barbados': 'BRB', 'Brunei Darussalam': 'BRN', 'Botswana': 'BWA', 'Central African Republic': 'CAF', 'Canada': 'CAN', 
'Switzerland': 'CHE', 'Chile': 'CHL', 'China': 'CHN', "Cote d'Ivoire": 'CIV', 'Cameroon': 'CMR', 'Congo, Dem. Rep.': 'CD', 'Congo, Rep.': 'COG', 'Colombia': 'COL', 'Comoros': 'COM', 'Cabo Verde': 'CPV', 'Costa Rica': 'CRI', 'Cuba': 'CUB', 'Cyprus': 'CYP', 'Czech Republic': 'CZE', 
'Germany': 'DEU', 'Djibouti': 'DJI', 'Dominica': 'DMA', 'Denmark': 'DNK', 'Dominican Republic': 'DOM', 'Algeria': 'DZA', 'Ecuador': 'ECU', 'Egypt, Arab Rep.': 'EGY', 'Eritrea': 'ERI', 'Spain': 'ESP', 'Estonia': 'EST', 'Ethiopia': 'ETH', 'European Union': 'EU', 'Finland': 'FIN', 'France': 'FRA', 
'Gabon': 'GAB', 'United Kingdom': 'GBR', 'Georgia': 'GEO', 'Ghana': 'GHA', 'Guinea': 'GIN', 'Gambia, The': 'GMB', 'Guinea-Bissau': 'GNB', 'Equatorial Guinea': 'GNQ', 'Greece': 'GRC', 'Grenada': 'GRD', 'Guatemala': 'GTM', 'Guyana': 'GUY', 
'Hong Kong SAR, China': 'HK','Honduras': 'HND', 'Croatia': 'HRV', 'Haiti': 'HTI', 'Hungary': 'HUN', 'Indonesia': 'IDN', 'India': 'IND', 'Ireland': 'IRL', 'Iran, Islamic Rep.': 'IRN', 'Iraq': 'IRQ', 'Iceland': 'ISL', 'Israel': 'ISR', 'Italy': 'ITA', 'Jamaica': 'JAM', 'Jordan': 'JOR', 'Japan': 'JPN', 'Kazakhstan': 'KAZ', 'Kenya': 'KEN', 
'Kyrgyz Republic': 'KGZ', 'Cambodia': 'KHM', 'Korea, Rep.': 'KOR', 'Kuwait': 'KWT', 'Lao PDR': 'LAO', 'Lebanon': 'LBN', 'Liberia': 'LBR', 'Libya': 'LBY', 'St. Lucia': 'LCA', 'Sri Lanka': 'LKA', 'Lesotho': 'LSO', 'Lithuania': 'LTU', 'Latvia': 'LVA', 'Macao SAR, China': 'MO', 'Morocco': 'MAR', 'Moldova': 'MDA', 'Madagascar': 'MDG', 'Mexico': 'MEX', 'North Macedonia': 'MKD', 'Mali': 'MLI', 'Malta': 'MLT', 'Myanmar': 'MMR', 'Montenegro': 'MNE', 'Mongolia': 'MNG', 'Mozambique': 'MOZ', 
'Mauritania': 'MRT', 'Mauritius': 'MUS', 'Malawi': 'MWI', 'Malaysia': 'MYS', 'Namibia': 'NAM', 'Nigeria': 'NGA', 'Nicaragua': 'NIC', 'Netherlands': 'NLD', 'Norway': 
'NOR', 'Nepal': 'NPL', 'New Zealand': 'NZL', 'Oman': 'OMN', 'Pakistan': 'PAK', 'Panama': 'PAN', 'Peru': 'PER', 'Philippines': 'PHL', 'Papua New Guinea': 'PNG', 'Poland': 'POL', 'Portugal': 'PRT', 'Paraguay': 'PRY', 'West Bank and Gaza': 'West Bank and Gaza', 'Qatar': 'QAT', 'Romania': 'ROU', 'Russian Federation': 'RUS', 'Rwanda': 'RWA', 
'Saudi Arabia': 'SAU', 'Sudan': 'SDN', 'Senegal': 'SEN', 'Singapore': 'SGP', 'Sierra Leone': 'SLE', 'El Salvador': 'SLV', 'San Marino': 'SMR', 'Somalia': 'SOM', 'Serbia': 'SRB', 'Sao Tome and Principe': 'STP', 'Suriname': 'SUR', 'Slovak Republic': 'SVK', 'Slovenia': 'SVN', 'Sweden': 'SWE', 'Eswatini': 'SWZ', 'Seychelles': 'SYC', 'Syrian Arab Republic': 'SYR', 'Chad': 'TCD', 'Togo': 'TGO', 'Thailand': 'THA', 'Tajikistan': 'TJK', 'Turkmenistan': 'TKM', 'Timor-Leste': 'TLS', 'Tonga': 
'TON', 'Trinidad and Tobago': 'TTO', 'Tunisia': 'TUN', 'Turkey': 'TUR', 'Tanzania': 'TZA', 'Uganda': 'UGA', 'Ukraine': 'UKR', 'Uruguay': 'URY', 'United States': 'USA', 'Uzbekistan': 'UZB', 'St. Vincent and the Grenadines': 'VCT', 'Venezuela, RB': 'VEN', 'Vietnam': 'VNM', 'Vanuatu': 'VUT', 'Yemen, Rep.': 'YEM', 'South Africa': 'ZAF', 'Zambia': 'ZMB', 'Zimbabwe': 'ZWE'}
WBdata.rename(index=converted_dict, inplace=True)

# Extract data from WBdata and place them in dataset
for index, rowDF in df.iterrows():
    year = str(rowDF['Year of signature'])
    party1 = df.loc[index, 'ISO-Party1']
    party2 = df.loc[index, 'ISO-Party2']

    if (party1 not in parties or party2 not in parties):
        pass
    else:
        #print(party1, year)
        #print(WBdata.loc[party1, year][0], WBdata.loc[party1, year][1])
        #print(WBdata.loc[party2, year][0], WBdata.loc[party2, year][1])

        df.loc[index, 'FDIOutflowsP1'] = np.round(WBdata.loc[party1, year][0], decimals=4)
        df.loc[index, 'FDIInflowsP1'] = np.round(WBdata.loc[party1, year][1], decimals=4)

        df.loc[index, 'FDIOutflowsP2'] = np.round(WBdata.loc[party2, year][0], decimals=4)
        df.loc[index, 'FDIInflowsP2'] = np.round(WBdata.loc[party2, year][1], decimals=4)


# Rearrange columns order
cols_to_order = [
                'score', 'Party1', 'Party2', 'ISO-Party1', 'ISO-Party2',
                'FDIOutflowsP1', 'FDIInflowsP1',
                'FDIOutflowsP2', 'FDIInflowsP2',
                'Year of signature','name', 'Parties'
                ]
new_columns = cols_to_order + (df.columns.drop(cols_to_order).tolist())
df = df[new_columns]

# Export to csv
df.to_csv('../data/5-added_variables.csv', index=False)
print('Done.')
