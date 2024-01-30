# from scrapy import cmdline
# cmdline.execute('scrapy crawl example'.split())

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from task1.spiders.new import NewHouseSpider
from task1.spiders.sec_hand import SecHandHouseSpider


configure_logging()
runner = CrawlerRunner()
runner.crawl(NewHouseSpider)
runner.crawl(SecHandHouseSpider)
runner.join().addBoth(lambda _:reactor.stop())
reactor.run()