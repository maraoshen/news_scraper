from twisted.internet import reactor
from twisted.internet import task

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from news_scraper.spiders.news_spider import NewsSpider


def run_crawler():
    runner = CrawlerRunner(get_project_settings())
    runner.crawl(NewsSpider)


def main():
    loop = task.LoopingCall(run_crawler)
    loop.start(3)
    reactor.run()


if __name__ == '__main__':
    main()
