from bs4 import BeautifulSoup
import requests
import json
import time

# strip contents of '\n'
def cleanN(el, parent):
    if isinstance(el, str):
        parent.contents.remove(el)
    return

t1 = time.time()

urls = []
with open('urls.txt', 'r') as f:
    for line in f:
        urls.append(line.strip())

#urls = ['https://investmentpolicy.unctad.org/international-investment-agreements/treaties/bit/64/algeria---italy-bit-1991-']
treaties = []

for i, url in enumerate(urls):
    i += 1

    print(f'Retrieving information: {i}/{len(urls)}')

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Informations per treaty
    information = {}
    
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

        lastCritLvl1 = None
        lastCritLvl2 = None

        # Loop through each row
        for row in rows:   
            # Clean list of \n       
            for el in row.contents:
                cleanN(el, row)
            
            # if only 1 child, create new dict, continue 
            if len(row.contents) == 1:
                if lastCritLvl1 is None:
                    BASE[row.contents[0].text.strip()] = {}
                    lastCritLvl1 = row.contents[0].text
                else:   
                    BASE[lastCritLvl1][row.contents[0].text.strip()] = {}  
                    lastCritLvl2 = row.contents[0].text
            
            # if there is 2 child div, key: value
            else:
                if lastCritLvl1 is None:
                    BASE[row.contents[0].text.strip()] = row.contents[1].text.strip()
                else:
                    nextElement = row.contents[0].parent.next_sibling.next_sibling

                    if lastCritLvl2 is None: 
                        BASE[lastCritLvl1][row.contents[0].text.strip()] = row.contents[1].text.strip()

                        if nextElement is not None:
                            # strip contents of '\n'
                            for el in nextElement:
                                cleanN(el, nextElement)

                            # it's a criteria        
                            if len(nextElement.contents) == 1:
                                if len(nextElement.contents[0]['class']) == 1:
                                    lastCritLvl1 = None
                    else:
                        BASE[lastCritLvl1][lastCritLvl2][row.contents[0].text.strip()] = row.contents[1].text.strip()

                        if nextElement is not None:
                            # strip contents of '\n'
                            for el in nextElement:
                                if isinstance(el, str):
                                    cleanN(el, nextElement)

                            # it's a criteria        
                            if len(nextElement.contents) == 1:
                                if len(nextElement.contents[0]['class']) == 1:
                                    lastCritLvl1 = None
                                    lastCritLvl2 = None
                                if len(nextElement.contents[0]['class']) == 2:
                                    lastCritLvl2 = None
    # Append to treaties dict                                
    treaties.append(information)
    time.sleep(0.5)

elapsed = time.time() - t1

print('Finished retrieving information in', elapsed, 's')
print('Writing to data.json')

with open('data.json', 'w') as outfile:
    json.dump(treaties, outfile)

print('Done.')
