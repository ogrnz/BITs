from bs4 import BeautifulSoup
import requests
import json
import time

def cleanN(el, parent):
    # Strip list of '\n' items
    if isinstance(el, str):
        parent.contents.remove(el)
    return

def isCrit(row):
    # Know if current row is a criteria
    isCrit = False
    if len(row.contents) == 1:
        isCrit = True
    return isCrit

def getRowLvl(row):
    # Get current depth lvl of row
    lvl = None
    if len(row.contents[0].attrs['class']) == 1:
        lvl = 0
    elif row.contents[0].attrs['class'][1] == 'col-sm-offset-1':
        lvl = 1
    elif row.contents[0].attrs['class'][1] == 'col-sm-offset-2':
        lvl = 2
    return lvl
    
t1 = time.time()

urls = []
with open('./helper/urls.txt', 'r') as f:
    for line in f:
        urls.append(line.strip())

## Dev 
#urls = ['https://investmentpolicy.unctad.org/international-investment-agreements/treaties/bit/58/algeria---finland-bit-2005-']
treaties = []

for i, url in enumerate(urls, start = 1):
    print(f'Retrieving information: {i}/{len(urls)}')

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Information per treaty
    information = {}
    
    # Treaty name
    information['name'] = soup.find('div', class_='page-title').h2.text.strip()

    # First elements
    firstEls = soup.find_all('div', class_="form-group")
    for el in firstEls:
        k = el.label.text.strip()
        v = el.next_element.next_element.next_element.next_element.next_element.text.strip()
        information[k] = v

    # Informations per criteria
    information['criteria'] = {}

    # Get panel headings "div.panel-heading", create dict for each section
    headings = soup.find_all('div', class_='panel-heading')

    for heading in headings:
        
        # Create criteria dict
        information['criteria'][heading.text.strip()] = {}
        BASE = information['criteria'][heading.text.strip()]

        # Get next sibling of each panel heading, those are sections 
        section = heading.next_sibling.next_sibling
        
        # Inside each section, get each div.row
        rows = section.find_all('div', class_='row')

        lastCritLvl0 = None
        lastCritLvl1 = None

        # Loop through each row
        for row in rows:   
            # Clean list of \n items      
            for el in row.contents:
                cleanN(el, row)
            
            # Get row current depth lvl
            currLvl = getRowLvl(row)

            # Row is a criteria
            if isCrit(row):
                if currLvl == 0:
                    BASE[row.contents[0].text.strip()] = {}
                    lastCritLvl0 = row.contents[0].text.strip()
                elif currLvl == 1:
                    BASE[lastCritLvl0][row.contents[0].text.strip()] = {}
                    lastCritLvl1 = row.contents[0].text.strip()
                else:   
                    BASE[lastCritLvl0][lastCritLvl1][row.contents[0].text.strip()] = {}

            # if there is 2 child div, key: value given depth of row
            else:
                if currLvl == 0:
                    BASE[row.contents[0].text.strip()] = row.contents[1].text.strip()
                elif currLvl == 1: 
                    BASE[lastCritLvl0][row.contents[0].text.strip()] = row.contents[1].text.strip()
                elif currLvl == 2:
                        BASE[lastCritLvl0][lastCritLvl1][row.contents[0].text.strip()] = row.contents[1].text.strip()

    # Append to treaties dict                                
    treaties.append(information)
    sleep = 0.2
    time.sleep(sleep)

elapsed = time.time() - t1
sleepingTime = sleep * len(treaties)

print('Finished retrieving information in', elapsed, 'sec')
print('That time takes into account the sleeping time in script which was', sleepingTime, 'sec')
print('Actual opreation time took', elapsed - sleepingTime, 'sec')

print('Writing result to data.json')
with open('./data/data.json', 'w') as outfile:
    json.dump(treaties, outfile)
print('Done.')