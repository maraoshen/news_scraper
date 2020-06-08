from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, Join, TakeFirst
from w3lib.html import replace_escape_chars, remove_tags


class Content(Item):
    url = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())
    date_scraped = Field(output_processor=TakeFirst())
    content = Field(
        input_processor=MapCompose(lambda v: v.strip(), remove_tags, replace_escape_chars),
        output_processor=Join(),
    )
