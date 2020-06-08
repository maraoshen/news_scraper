from urllib.parse import urlparse

from scrapy import Spider
from scrapy.loader import ItemLoader

from news_scraper.items import Content


class NewsSpider(Spider):
    name = "news"
    start_urls = [
        'https://news.abs-cbn.com/'
    ]

    def parse(self, response):

        loader = ItemLoader(item=Content(), response=response)
        loader.add_value('url', response.request.url)
        loader.add_value('name', urlparse(response.url).netloc)
        loader.add_xpath('content', '//*[not(self::script)]/text()')

        return loader.load_item()
