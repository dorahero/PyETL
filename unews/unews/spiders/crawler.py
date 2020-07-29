import scrapy
from scrapy import Request, FormRequest
from bs4 import BeautifulSoup
from unews.items import UnewsItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json
import time
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
class UnewsCrawler(scrapy.Spider):
    name = 'unews'
    # url = 'https://autos.udn.com/autos/ajax_article/{}/-1/7825?_={}'.format(p + 700, p + 700)
    start_urls = ['https://autos.udn.com/autos/ajax_article/{}/-1/12168?_={}'.format(p+1, p+1) for p in range(300)]
    def parse(self, response):
        domain = 'https://autos.udn.com'
        soup = BeautifulSoup(response.body)
        for soup_h in soup.select('a'):
            yield scrapy.Request(domain + soup_h['href'], self.parse_detail)
    def parse_detail(self, response):
        res = BeautifulSoup(response.body)
        unewsitem = UnewsItem()
        unewsitem['title'] = res.select('#story_art_title')[0].text
        unewsitem['text'] = str([s.text for s in res.select('div[id="story_body_content"]')[0].select('p')])\
            .replace('[', '').replace('\'', '')\
            .replace(', ', '').replace(']', '')
        unewsitem['time'] = res.select('div[id="story_body_content"]')[0].select('span')[0].text
        return unewsitem
