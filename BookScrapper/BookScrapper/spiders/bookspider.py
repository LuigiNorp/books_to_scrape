from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from itemloaders.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from BookScrapper.items import Book
from random import choice
import re

# To select another category randomly

categories = [  "Travel" , "Mystery" , "Historical-Fiction" , "Sequential-Art" , 
                "Classics" , "Philosophy" , "Romance" , "Womens-Fiction" , "Fiction" , 
                "Childrens" , "Religion" , "Nonfiction" , "Music" , "Default" , 
                "Science-Fiction" , "Sports-and-Games" , "Add-a-comment" , "Fantasy" , 
                "New-Adult" , "Young-Adult" , "Science" , "Poetry" , "Paranormal" , "Art" , 
                "Psychology" , "Autobiography" , "Parenting" , "Adult-Fiction" , "Humor" , 
                "Horror" , "History" , "Food-and-Drink" , "Christian-Fiction" , "Business" , 
                "Thriller" , "Contemporary" , "Spirituality" , "Academic" , "Self-Help" , 
                "Historical" , "Christian" , "Suspense" , "Short-Stories" , "Novels" , 
                "Health" , "Politics" , "Cultural" , "Erotica" , "Crime"]

searched_category = ['biography']
searched_category.append(choice(categories).lower())
print(searched_category)

class BookSpider(CrawlSpider):
    name = 'bookspider'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    rules = (
        Rule(
            LinkExtractor(allow=fr'/{searched_category[0]}_\d+/'),
            follow=True,
            callback='open_book_details'),
        Rule(
            LinkExtractor(allow=fr'/{searched_category[1]}_\d+/'),
            follow=True,
            callback='open_book_details'),
    )

    def open_book_details(self, response):
        books = response.xpath('//ol//li//h3//a')
        for book in books:
            yield response.follow(book, callback=self.parse_book_details)


    def get_stock_info(self, texto):
        pattern = re.findall(r'\d+', texto)
        if len(pattern) > 0:
            return int(pattern[0])

    def get_rating_info(self, text):
        ratings = {
            'star-rating One':float(1),
            'star-rating Two':float(2),
            'star-rating Three':float(3),
            'star-rating Four':float(4),
            'star-rating Five':float(5),
        }
        return ratings[text]
    
    def price_str_to_float(self, text):
        return float(text.replace('£',''))

    def parse_book_details(self, response):
        sel = Selector(response)
        item = ItemLoader(Book(), sel)
        item.add_xpath('title','//h1/text()')
        item.add_xpath('category','//li[3]/a/text()')
        item.add_xpath('upc','//th[contains(text(),"UPC")]/following-sibling::td/text()')
        item.add_xpath('price','(//p[contains(@class,"price")])[1]/text()', MapCompose(self.price_str_to_float))
        item.add_xpath('stock','(//div[contains(@class,"main")]//p[contains(@class,"stock")])[1]/text()', MapCompose(self.get_stock_info))
        item.add_xpath('rating','//div[contains(@class,"main")]//p[contains(@class,"star-rating")]/@class', MapCompose(self.get_rating_info))
        yield item.load_item()