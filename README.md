# news_scraper
A scraper to scan for changes on a news website using python3, scrapy and sqlite.

## Installation
Create a virtual environment and install the requirements by running `pip install -r requirements.txt`

## Running the script
Run the command `python scheduler.py`

## Adding url to be scraped
On `news_scraper/spiders/news_spider.py` add the new url to `start_urls` list. Currently it is only scraping for `https://news.abs-cbn.com/`

## Changing the time to loop call
Currently, the script crawls the page every 3 seconds. In `scheduler.py` change the number inside `loop.start()` 

## Future Plans
Some settings are hardcoded that can be added as optional arguments when running the script
1. time for looping script
2. list of urls to scrape
3. enabling debug logs
