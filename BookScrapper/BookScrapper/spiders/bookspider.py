from scrapy.spiders import Spider
from scrapy.selector import Selector
from itemloaders.processors import MapCompose
from scrapy.loader import ItemLoader
from BookScrapper.items import Book
from random import choices
import re

class BookSpider(Spider):
    name = 'bookspider'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    
    custom_settings = {
        'FEEDS':{
            'libros.csv': {
                'format': 'csv'
            },
            'libros.json':{
                'format': 'json'
            }
        }
    }
    
    def parse(self, response):
        sel = Selector(response)
        categories_list =sel.xpath('(//ul)[2]//ul//a/@href').extract()
        two_categories=[]
        for cat in categories_list:
            if cat.__contains__('/biography_'):
                two_categories.append(f'http://books.toscrape.com/{cat}')
        two_categories.append(f'http://books.toscrape.com/{choices(categories_list)[0]}')
        for category in two_categories:
            
            yield response.follow(category, callback=self.open_book_details)

    def open_book_details(self, response):
        books = response.xpath('//ol//li//h3//a')
        for book in books:
            yield response.follow(book, callback=self.parse_book_details)

    def clean_categories(self, texto:str):
        categories = texto
        return categories

    def get_stock_info(self, texto:str):
        pattern = re.findall(r'\d+', texto)
        if len(pattern) > 0:
            return int(pattern[0])

    def get_rating_info(self, text:str):
        ratings = {
            'star-rating One':float(1),
            'star-rating Two':float(2),
            'star-rating Three':float(3),
            'star-rating Four':float(4),
            'star-rating Five':float(5),
        }
        return ratings[text]
    
    def price_str_to_float(self, text:str):
        return float(text.replace('£',''))

    def convert_to_url(self, src:str):
        return src.replace('../../', self.start_urls[0])

    def parse_book_details(self, response):
        sel = Selector(response)
        item = ItemLoader(Book(), sel)
        item.add_xpath('title','//h1/text()')
        item.add_xpath('category','//li[3]/a/text()')
        item.add_xpath('upc','//th[contains(text(),"UPC")]/following-sibling::td/text()')
        item.add_xpath('price','(//p[contains(@class,"price")])[1]/text()', MapCompose(self.price_str_to_float))
        item.add_xpath('stock','(//div[contains(@class,"main")]//p[contains(@class,"stock")])[1]/text()', MapCompose(self.get_stock_info))
        item.add_xpath('rating','//div[contains(@class,"main")]//p[contains(@class,"star-rating")]/@class', MapCompose(self.get_rating_info))
        item.add_xpath('image_url', '(//img)[1]/@src', MapCompose(self.convert_to_url))
        src = response.xpath('(//img)[1]/@src').get()
        url = self.convert_to_url(src)
        yield item.load_item()