# BITs scraper

Script to scrape content of mapped BITs (Bilateral Investment Treaties):
https://investmentpolicy.unctad.org/international-investment-agreements/iia-mapping

The data of the upper link is formatted as a python list in the `helper/cleaned_rows.py` file. This list was last updated on 13/02/2020 (dd/mm/yy). Please be aware that new treaties are regularly added, so you should scrape it again to have the latest data.

The mapped content of each treaty is then scraped using `scraper/script.py`. All data are then converted into a file named `data/data.json`.

If you wish to use the data in a `<html>` table, feel free to use the `helper/rows-generator.py` script to generate html code.

## TODO
Gotta format data.json into a csv file to be usable on R and such.