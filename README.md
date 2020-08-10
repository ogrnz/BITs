# International Investment Agreements scraper [Work in progress]
*Author: Laura Mauricio*

*Collaborator: Potrac*

*This repository is the coding-part of an academic project, which link will be published here once it's finished.*

This repository has two goals:
* Scraping the data off the UNCTAD Investement policy hub
* Analyzing and changing the dataset

The datasets are all available in the `data/` directory. 

## Scraping the data `scraper/`
Script to scrape content of mapped BITs & TIPs (Bilateral Investment Treaties & Treaties with Investment Provisions):
https://investmentpolicy.unctad.org/international-investment-agreements/iia-mapping

The data of the upper link is formatted as a python list in the `helper/cleaned_rows.py` file. This list was last updated on 13/02/2020 (dd/mm/yy). Please be aware that new treaties are regularly added, so you should scrape it again to have the latest data.

The mapped content of each treaty is scraped using `scraper/script.py`. All data are then converted into a file named `data/data.json`. This json fil was then converted into a csv, see `data/data.csv`.

## Managing the dataset `helper/`
Each script is performing one operation (or one kind of operation). The scripts are meant to be executed in order. The main library used is `pandas`. 

As of now, the last dataset is `data/8-polity_vars_added.csv`. Just take the file with the highest number.

### Misc
* If you wish to use the data in a `<html>` table, feel free to use the `helper/rows_generator.py` script to generate html code. 
* If you want to reproduce the steps, install the correct python packages with Pip:
`pip install -r requirements.txt`
* Script 3 `3-to_iso.py` takes a long time to run. It's normal.
* We are in no way CS students or something similar, the code is not elegant, but hey, it works.

Use it as you wish 🙂!
