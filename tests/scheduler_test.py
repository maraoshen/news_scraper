from unittest import TestCase
from unittest.mock import patch

from scheduler import run_crawler, main, LOOP_IN_SECONDS
from news_scraper.spiders.news_spider import NewsSpider


class SchedulerTest(TestCase):

    @patch('scheduler.get_project_settings')
    @patch('scheduler.CrawlerRunner')
    def test_run_crawler(self, mock_CrawlerRunner, mock_get_project_settings):
        run_crawler()

        mock_get_project_settings.assert_called_once()
        mock_CrawlerRunner.assert_called_with(mock_get_project_settings.return_value)
        mock_CrawlerRunner().crawl.assert_called_with(NewsSpider)

    @patch('scheduler.task.LoopingCall')
    @patch('scheduler.reactor.run')
    def test_main(self, mock_run, mock_LoopingCall):
        main()

        mock_LoopingCall.assert_called_with(run_crawler)
        mock_LoopingCall().start.assert_called_with(LOOP_IN_SECONDS)
        mock_run.assert_called_once()
