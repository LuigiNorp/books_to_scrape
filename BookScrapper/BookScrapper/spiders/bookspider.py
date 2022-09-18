from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.selector import Selector
from itemloaders.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from BookScrapper.items import Book, Images
import re

categorias_a_buscar = ['biography']
categorias_a_buscar.append(input('Ingresa una categoría a buscar: ').lower())

class BookSpider(CrawlSpider):
    name = 'bookspider'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    rules = (
        Rule(
            LinkExtractor(allow=fr'/{categorias_a_buscar[0]}_\d+/'),
            follow=True,
            callback='open_book_details'),
        Rule(
            LinkExtractor(allow=fr'/{categorias_a_buscar[1]}_\d+/'),
            follow=True,
            callback='open_book_details'),
    )

    def open_book_details(self, response):
        links_libros_en_categoria = response.xpath('//ol//li//h3//a')
        for libro in links_libros_en_categoria:
            yield response.follow(libro, callback=self.parse_book_details)


    def get_stock_info(self, texto):
        pattern = re.findall(r'\d+', texto)
        if len(pattern) > 0:
            return int(pattern[0])

    def get_rating_info(self, texto):
        ratings = {
            'star-rating One':float(1),
            'star-rating Two':float(2),
            'star-rating Three':float(3),
            'star-rating Four':float(4),
            'star-rating Five':float(5),
        }
        return ratings[texto]
    
    def price_str_to_float(self, texto):
        return float(texto.replace('£',''))

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

class ImageScraperSpider(CrawlSpider):
    name = 'imageSpider'
    # allowed_domains = ['books.toscrape.com/']
    # start_urls = ['http://books.toscrape.com/catalogue/louisa-the-extraordinary-life-of-mrs-adams_818/index.html']

    def parse(self, response):
        item = Images()
        if response.status == 200:
            rel_img_urls = response.xpath("//div[@class='item active']//img/@src").extract()
            item['image_urls'] = self.url_join(rel_img_urls, response)
        return item

    def url_join(self, rel_img_urls, response):
        joined_urls = []
        for rel_img_url in rel_img_urls:
            joined_urls.append(response.urljoin(rel_img_url))

        return joined_urls