from bs4 import BeautifulSoup
import requests
import json
import sys

url = 'https://investmentpolicy.unctad.org/international-investment-agreements/treaties/bit/3074/venezuela-bolivarian-republic-of---viet-nam-bit-2008-'

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# First elements
firstScrap = soup.find_all('p', class_="form-control-static")
desc = []
for el in firstScrap[0:4]:
    desc.append(el.text.strip())

def getAnswers(section_id):
    answers = []
    block = soup.find('div', id=section_id)
    values = block.find_all('div', class_='row')

    for row in values:
        row_content = row.find('div', class_='col-sm-4')
        if row_content is None:
            continue
        answers.append(row_content.text)
    return answers

treaties = {}

# Description
treaties['id'] = 0
treaties['name'] = soup.find('div', class_='page-title').h2.text
treaties['TreatyType'] = desc[0]
treaties['Status'] = desc[1]
treaties['DateSignature'] = desc[2]
treaties['DateEntry'] = desc[3]

# Criteria
treaties['criteria'] = {}

# Preamble 
PreambleValues = getAnswers('section_1')
treaties['criteria']['Preamble'] = {}
treaties['criteria']['Preamble']['Reference to right to regulate (e.g. regulatory autonomy, policy space, flexibility to introduce new regulations)'] = PreambleValues[0]
treaties['criteria']['Preamble']['Reference to sustainable development'] = PreambleValues[1]
treaties['criteria']['Preamble']['Reference to social investment aspects (e.g. human rights, labour, health, CSR, poverty reduction)'] = PreambleValues[2]
treaties['criteria']['Preamble']['Reference to environmental aspects (e.g. plant or animal life, biodiversity, climate change)'] = PreambleValues[3]

# Scope and Definitions 
ScopeDefinitionsValues = getAnswers('section_6')
treaties['criteria']['Scope and Definitions'] = {}
treaties['criteria']['Scope and Definitions']['Definition of investment'] = {}
treaties['criteria']['Scope and Definitions']['Definition of investment']['Type of definition'] = ScopeDefinitionsValues[0]
treaties['criteria']['Scope and Definitions']['Definition of investment']['Limitations to the definition of investment'] = {}
treaties['criteria']['Scope and Definitions']['Definition of investment']['Limitations to the definition of investment']['Excludes portfolio investment'] = ScopeDefinitionsValues[1]
treaties['criteria']['Scope and Definitions']['Definition of investment']['Limitations to the definition of investment']['Excludes other specific assets (e.g. sovereign debt, ordinary commercial transactions, etc.)'] = ScopeDefinitionsValues[2]
treaties['criteria']['Scope and Definitions']['Definition of investment']['Limitations to the definition of investment']['Lists required characteristics of investment'] = ScopeDefinitionsValues[3]
treaties['criteria']['Scope and Definitions']['Definition of investment']['Limitations to the definition of investment']['Contains "in accordance with host State laws" requirement'] = ScopeDefinitionsValues[4]
treaties['criteria']['Scope and Definitions']['Definition of investment']['Limitations to the definition of investment']['Sets out closed (exhaustive) list of covered assets'] = ScopeDefinitionsValues[5]

treaties['criteria']['Scope and Definitions']['Definition of investor'] = {}
treaties['criteria']['Scope and Definitions']['Definition of investor']['Definition included'] = ScopeDefinitionsValues[6]
treaties['criteria']['Scope and Definitions']['Definition of investor']['Specifying natural persons covered'] = {}
treaties['criteria']['Scope and Definitions']['Definition of investor']['Specifying natural persons covered']['Includes permanent residents'] = ScopeDefinitionsValues[7] 
treaties['criteria']['Scope and Definitions']['Definition of investor']['Specifying natural persons covered']['Excludes dual nationals'] = ScopeDefinitionsValues[8]
treaties['criteria']['Scope and Definitions']['Definition of investor']['Specifying legal entities covered'] = {}
treaties['criteria']['Scope and Definitions']['Definition of investor']['Specifying legal entities covered']['Includes requirement of substantial business activity'] = ScopeDefinitionsValues[9] 
treaties['criteria']['Scope and Definitions']['Definition of investor']['Specifying legal entities covered']['Defines ownership and control of legal entities'] = ScopeDefinitionsValues[10]

treaties['criteria']['Scope and Definitions']['Denial of benefits (DoB)'] = {}
treaties['criteria']['Scope and Definitions']['Denial of benefits (DoB)']['DoB clause included'] = ScopeDefinitionsValues[11]
treaties['criteria']['Scope and Definitions']['Denial of benefits (DoB)']['Content of the DoB clause'] = {}
treaties['criteria']['Scope and Definitions']['Denial of benefits (DoB)']['Content of the DoB clause']['"Substantive business operations" criterion'] = ScopeDefinitionsValues[12]
treaties['criteria']['Scope and Definitions']['Denial of benefits (DoB)']['Content of the DoB clause']['Applies to investors from States with no diplomatic relations or under economic/trade restrictions'] = ScopeDefinitionsValues[13]
treaties['criteria']['Scope and Definitions']['Denial of benefits (DoB)']['Content of the DoB clause']['Discretionary ("Party may deny") or mandatory ("benefits shall be denied")'] = ScopeDefinitionsValues[14]

treaties['criteria']['Scope and Definitions']['Substantive scope of the treaty'] = {}
treaties['criteria']['Scope and Definitions']['Substantive scope of the treaty']['Limiting substantive scope of the treaty'] = {}
treaties['criteria']['Scope and Definitions']['Substantive scope of the treaty']['Limiting substantive scope of the treaty']['Excludes taxation'] = ScopeDefinitionsValues[15]
treaties['criteria']['Scope and Definitions']['Substantive scope of the treaty']['Limiting substantive scope of the treaty']['Excludes subsidies, grants'] = ScopeDefinitionsValues[16]
treaties['criteria']['Scope and Definitions']['Substantive scope of the treaty']['Limiting substantive scope of the treaty']['Excludes government procurement'] = ScopeDefinitionsValues[17]
treaties['criteria']['Scope and Definitions']['Substantive scope of the treaty']['Limiting substantive scope of the treaty']['Excludes other subject matter'] = ScopeDefinitionsValues[18]

treaties['criteria']['Scope and Definitions']['Temporal scope of the treaty'] = {}
treaties['criteria']['Scope and Definitions']['Temporal scope of the treaty']['Investments covered'] = ScopeDefinitionsValues[19]
treaties['criteria']['Scope and Definitions']['Temporal scope of the treaty']['Disputes covered'] = ScopeDefinitionsValues[20]

# Standards of Treatment 

# CHECK if len(answers) == last index used
#print(json.dumps(treaties), len(ScopeDefinitionsValues))
