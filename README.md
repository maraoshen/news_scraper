# news_scraper
A scraper to scan for changes on a news website using python3, scrapy and sqlite.

## Installation
Create a virtual environment and install the requirements by running `pip install -r requirements.txt`

## Running the script
Run the command `python scheduler.py [--loop SEC]`. 
If loop argument is not provided, the script will run by default every 60 seconds.

## Adding url to be scraped
On `news_scraper/spiders/news_spider.py` add the new url to `start_urls` list. 
Currently it is only scraping for `https://news.abs-cbn.com/`

## Future Plans
Some settings are hardcoded that can be added as optional arguments when running the script or fetched from the backend
1. list of urls to scrape
2. enabling debug logs
