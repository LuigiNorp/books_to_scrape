from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


# categoria = str(input('Escriba una categoria a scrapear: ')).lower()

class Book(Item):
    """Esta clase contiene la información de los campos 

    Args:
        Item (_type_): _description_
    """
    titulo = Field()
    categoria = Field()
    upc = Field()
    precio = Field()
    stock = Field()
    rating = Field()

class BooksToScrape(CrawlSpider):
    name = 'BooksFromBooksToScrape'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.132 Safari/537.36',

        'CLOSESPIDER_PAGECOUNT': 50
    }
    allowed_domains = ['toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    download_delay = 1

    rules = (
        # Biography category
        Rule(
            LinkExtractor(allow=r'/biography_\d+/'),
            follow=True
        ),

        Rule(
            LinkExtractor(
                allow=r'/catalogue/',
                restrict_xpaths=['//ol']),
            follow=True,
            callback='parse_book'
        ),
    )

    def obtener_stock(self, texto):
        return str(texto)

    def obtener_calificacion(self, texto):
        ratings = {
            'star-rating One':1.00,
            'star-rating Two':2.00,
            'star-rating Three':3.00,
            'star-rating Four':4.00,
            'star-rating Five':5.00,
        }
        return ratings[texto]
    
    def limpiar_precio(self, texto):
        return float(texto.replace('£',''))


    def parsear_libro(self, response):
        sel = Selector(response)
        item = ItemLoader(Book(), sel)
        item.add_xpath('titulo','//h1/text()')
        item.add_xpath('categoria','//li[3]/a/text()')
        item.add_xpath('upc','//th[contains(text(),"UPC")]/following-sibling::td/text()')
        item.add_xpath('precio','(//p[contains(@class,"price")])[1]/text()', MapCompose(self.limpiar_precio))
        item.add_xpath('stock','(//div[contains(@class,"main")]//p[contains(@class,"stock")])[1]/text()', MapCompose(self.obtener_stock))
        item.add_xpath('rating','//div[contains(@class,"main")]//p[contains(@class,"star-rating")]/@class', MapCompose(self.obtener_calificacion))


        yield item.load_item()


# To run without terminal
# This is equivalent to write in terminal:
# scrapy runspider file_name -o results.ext -t ext
process = CrawlerProcess(settings={
    "FEEDS": {"libros.csv": {"format": "csv"},
              },
})

process.crawl(BooksToScrape)
process.start() # the script will block here until the crawling is finished