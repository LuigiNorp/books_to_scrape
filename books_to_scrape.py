from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
import re


categorias_a_buscar = ['biography']
categorias_a_buscar.append(input('Ingresa una categoría a buscar: ').lower())

class Book(Item):
    titulo = Field()
    categoria = Field()
    upc = Field()
    precio = Field()
    stock = Field()
    rating = Field()
    url_imagen = Field()
    imagen = Field()

class BookSpider(CrawlSpider):
    name = 'books'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.132 Safari/537.36',
    }
    allowed_domains = ['toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    download_delay = 1

    rules = (
        Rule(
            LinkExtractor(allow=fr'/{categorias_a_buscar[0]}_\d+/'),
            follow=True,
            callback='ingresar_a_libros'),
        Rule(
            LinkExtractor(allow=fr'/{categorias_a_buscar[1]}_\d+/'),
            follow=True,
            callback='ingresar_a_libros'),
    )

    def obtener_imagen(self, response):
        links_libros_en_categoria = response.xpath('//ol//li//h3//a')
        for libro in links_libros_en_categoria:
            pass


    def ingresar_a_libros(self, response):
        links_libros_en_categoria = response.xpath('//ol//li//h3//a')
        for libro in links_libros_en_categoria:
            yield response.follow(libro, callback=self.parsear_libro)

    def obtener_stock(self, texto):
        pattern = re.findall(r'\d+', texto)
        if len(pattern) > 0:
            return int(pattern[0])

    def obtener_calificacion(self, texto):
        ratings = {
            'star-rating One':float(1),
            'star-rating Two':float(2),
            'star-rating Three':float(3),
            'star-rating Four':float(4),
            'star-rating Five':float(5),
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
    "FEEDS": {
        "libros.csv": {"format": "csv"},
        "libros.json":{"format":"json"},
              },
})

process.crawl(BookSpider)
process.start() # the script will block here until the crawling is finished