from scrapy.spiders import CrawlSpider, Spider
from BookScrapper.settings import URLS_LIST
from BookScrapper.items import Images
from scrapy.http import Response

class ImageSpider(Spider):
    name = 'imagespider'
    allowed_domains = ['books.toscrape.com/']
    start_urls =  URLS_LIST
    def __init__(self):
        item = Images()
        for src in self. start_urls:
            response = Response(src)
            print(response)
            item['image_urls'] = self.urljoin(src, response)
        yield item
    
    # def parse(self, response):
    #     if response.status == 200:
    #         src = response.xpath("//div[@class='item active']//img/@src").extract()
    #         item['image_urls'] = self.url_join(src, response)
    #     return item

    def url_join(self, sources, response):
        joined_urls = []
        for src in sources:
            joined_urls.append(response.urljoin(src))

    #     return joined_urls
    
