import scrapy
from scrapy import Request, FormRequest
from bs4 import BeautifulSoup
from king.items import KingItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json
import time
class KingCrawler(scrapy.Spider):
    name = 'king'
    # url = 'https://autos.udn.com/autos/ajax_article/{}/-1/7825?_={}'.format(p + 700, p + 700)
    start_urls = ['https://www.kingautos.net/all/page{}'.format(p+1) for p in range(2281)]
    def parse(self, response):
        domain = 'https://www.kingautos.net'
        soup = BeautifulSoup(response.body)
        for i, h in enumerate(soup.select('div[class="kind"]')[0].select('a')):
            if len(h['href']) < 10 and i % 3 == 0:
                yield scrapy.Request(domain + h['href'], self.parse_detail)
    def parse_detail(self, response):
        res = BeautifulSoup(response.body)
        kingitem = KingItem()
        kingitem['title'] = res.select('div[class="article"]')[0].select('h1')[0].text
        kingitem['text'] = str([s.text for s in res.select('div[class="articleContent"]')[0].select('p')]) \
            .replace('[', '').replace('\'', '') \
            .replace(', ', '').replace(']', '')
        kingitem['time'] = res.select('div[class="author"]')[0].select('.date')[0].text.split('on ')[1]
        if len(kingitem['text']) > 0:
            return kingitem
        return None