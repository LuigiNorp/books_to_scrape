from BookScrapper.spiders import bookspider, imagespider
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(bookspider.BookSpider)
    # yield runner.crawl(imagespider.ImageSpider) # TODO: Se comentó porque no se ejecuta correctamente
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished