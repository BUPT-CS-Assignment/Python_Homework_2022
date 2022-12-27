# from scrapy import cmdline
# cmdline.execute('scrapy crawl example'.split())

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from core.spiders.cbd import CBDSpider
from core.spiders.renting import RentingSpider
import multiprocessing
from core.base import citys
import time

def config_on():
    configure_logging()

def cbd_crawler():
    runner = CrawlerRunner()        
    for city in citys:
        runner.crawl(CBDSpider, city=city)
    runner.join().addBoth(lambda _:reactor.stop())
    reactor.run()
    print('done.')
    
def renting_crawler():
    runner = CrawlerRunner()        
    for city in citys:
        runner.crawl(RentingSpider, city=city)
    runner.join().addBoth(lambda _:reactor.stop())
    reactor.run()


# main crwaler api
def catch(recap_cbd = False):
    start = time.time()
    targets = [cbd_crawler] if recap_cbd else []
    targets.append(renting_crawler)
    for t in targets:
        p = multiprocessing.Process(target=t)
        p.start()
        p.join()
    end = time.time()
    print(f'crawling finished in {end - start} sec')