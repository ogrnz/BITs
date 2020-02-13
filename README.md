# BITs

Script to scrape content of mapped BITs (Bilateral Investment Treaties):
https://investmentpolicy.unctad.org/international-investment-agreements/iia-mapping

The data of the upper link is formatted as a python list in the cleaned_rows.py file. This list was last updated on 13/02/2020 (dd/mm/yy). Please be aware that new treaties are regularly added.

The mapped content of each treaty is then scraped using script1.py. All data are then converted into a json file: data.json.