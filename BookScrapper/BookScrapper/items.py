# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item

class Book(Item):
    title = Field()
    category = Field()
    upc = Field()
    price = Field()
    stock = Field()
    rating = Field()

class Images(Item):
    image_name = Field()
    image_urls = Field()
    images = Field()