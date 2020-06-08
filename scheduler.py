import argparse

from twisted.internet import reactor
from twisted.internet import task

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from news_scraper.spiders.news_spider import NewsSpider


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loop", help="Loop call in seconds.", type=float, default=3.)

    args = parser.parse_args()

    return args


def run_crawler():
    runner = CrawlerRunner(get_project_settings())
    runner.crawl(NewsSpider)


def main(loop=3):
    loop_call = task.LoopingCall(run_crawler)
    loop_call.start(loop)
    reactor.run()


if __name__ == '__main__':
    args = parse_arguments()

    main(args.loop)
