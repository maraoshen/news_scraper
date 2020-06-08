from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from news_scraper.pipelines import SQLiteDatabasePipeline


class PipelinesTest(TestCase):
    def setUp(self):
        mock_connect = patch('news_scraper.pipelines.sqlite3.connect')
        self.connect = mock_connect.start()
        self.addCleanup(mock_connect.stop)

        mock_cursor = patch('news_scraper.pipelines.sqlite3.connect.cursor')
        self.cursor = mock_cursor.start()
        self.addCleanup(mock_cursor.stop)

        self.spider = MagicMock()
        self.item = {'url':"url.com", 'content':"content", "name":"name"}

    @patch('news_scraper.pipelines.get_project_settings')
    def test_open_spider(self, mock_get_project_settings):
        connect_str = 'constr'
        mock_get_project_settings.return_value = {"CONNECTION_STRING": connect_str}

        SQLiteDatabasePipeline().open_spider(self.spider)

        mock_get_project_settings.assert_called_once()
        self.connect.assert_called_with(connect_str)
        self.connect().cursor.assert_called()
        self.connect().cursor().execute.assert_called_with(
            'CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY, url TEXT, name TEXT, date_scraped TEXT DEFAULT CURRENT_TIMESTAMP, content TEXT)'
        )

    def test_close_spider(self):
        pipeline = SQLiteDatabasePipeline()
        pipeline.connection = self.connect
        pipeline.close_spider(self.spider)

        pipeline.connection.commit.assert_called_once()
        pipeline.connection.close.assert_called_once()

    def test_process_item_no_changes(self):
        pipeline = SQLiteDatabasePipeline()
        pipeline.cursor = self.cursor
        pipeline.cursor.fetchone.return_value = True

        res = pipeline.process_item(self.item, self.spider)

        pipeline.cursor.execute.assert_called_with(
            "select * from news where url=? and content=?", (self.item['url'], self.item['content'])
        )
        pipeline.cursor.fetchone.assert_called_once()
        self.assertEqual(res, self.item)

    def test_process_item_first_item(self):
        pipeline = SQLiteDatabasePipeline()
        pipeline.cursor = self.cursor
        pipeline.cursor.fetchone.return_value = False

        res = pipeline.process_item(self.item, self.spider)

        sql = "insert into news(url, name, content) values(?, ?, ?)"
        calls = [
            call("select * from news where url=? and content=?", (self.item['url'], self.item['content'])),
            call("select content from news where id in (select max(id) from news)"),
            call(sql, (self.item['url'], self.item['name'], self.item['content']))
        ]
        pipeline.cursor.execute.assert_has_calls(calls)
        self.assertEqual(res, self.item)

    def test_process_item_compare_changes(self):
        pipeline = SQLiteDatabasePipeline()
        pipeline.cursor = self.cursor
        pipeline.cursor.fetchone.side_effect = [False, ("old content", )]

        res = pipeline.process_item(self.item, self.spider)
        self.assertEqual(res, self.item)
