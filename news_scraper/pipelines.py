import logging
import sqlite3
import re
from difflib import Differ

from scrapy.utils.project import get_project_settings


class SQLiteDatabasePipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect(get_project_settings().get("CONNECTION_STRING"))
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY, url TEXT, name TEXT, date_scraped TEXT DEFAULT CURRENT_TIMESTAMP, content TEXT)'
        )

    def process_item(self, item, spider):
        self.cursor.execute("select * from news where url=? and content=?", (item['url'], item['content']))
        result = self.cursor.fetchone()
        if result:
            logging.debug("No new changes.")
            print('No new changes.')
        else:
            self.cursor.execute("select content from news where id in (select max(id) from news)")
            old_content = self.cursor.fetchone()
            if old_content:
                old_content = re.sub("\s{2,}", "\n", old_content[0]).splitlines(keepends=True)
                new_content = re.sub("\s{2,}", "\n", item['content']).splitlines(keepends=True)
                result = list(Differ().compare(new_content, old_content))
                text_diff = ''.join(line for line in result if not line.startswith(' '))
                print(text_diff)

            sql = "insert into news(url, name, content) values(?, ?, ?)"
            self.cursor.execute(sql, (item['url'], item['name'], item['content']))
            logging.debug("Item stored")
        return item

    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()
