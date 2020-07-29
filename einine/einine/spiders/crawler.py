import scrapy
from scrapy import Request, FormRequest
from bs4 import BeautifulSoup
from einine.items import EinineItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json
import time
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
class EinineCrawler(scrapy.Spider):
    name = 'einine'
    start_urls = ['https://c.8891.com.tw/api/v2/pcArticle?page={}'.format(i+1) for i in range(500)]
    def parse(self, response):
        j_data = json.loads(response.body)
        for j in j_data['data']['list']:
            # print(j['link'])
            yield scrapy.Request(j['link'], self.parse_detail)
    def parse_detail(self, response):
        res = BeautifulSoup(response.body)
        einineitem = EinineItem()
        einineitem['title'] = res.select('div.carTypDetail')[0].text.split('作者')[0].replace('\n', '')
        einineitem['text'] = res.select('#article-box')[0].text
        einineitem['time'] = res.select('.insidePageTime')[0].text
        if len(einineitem['text']) > 0:
            return einineitem
        else:
            return None

# class EinineCrawler(CrawlSpider):
#     name = 'einine'
#     # allowed_domains = ['c.8891.com.tw']
#     start_urls = ['https://c.8891.com.tw/api/v2/pcArticle?page=1']
#     # login_page = 'https://c.8891.com.tw/api/v2/pcArticle'
#     # def start_requests(self):
#     #     for u in self.start_urls:
#     #         yield scrapy.Request(u, callback=self.parse_httpbin,
#     #                                 errback=self.errback_httpbin,
#     #                                 dont_filter=True)
#     #
#     # def parse_httpbin(self, response):
#     #     self.logger.error('Got successful response from {}'.format(response.url))
#     #     # do something useful now
#     #
#     # def errback_httpbin(self, failure):
#     #     # log all errback failures,
#     #     # in case you want to do something special for some errors,
#     #     # you may need the failure's type
#     #     self.logger.error(repr(failure))
#     #
#     #     # if isinstance(failure.value, HttpError):
#     #     if failure.check(HttpError):
#     #         # you can get the response
#     #         response = failure.value.response
#     #         self.logger.error('HttpError on %s', response.url)
#     #
#     #     # elif isinstance(failure.value, DNSLookupError):
#     #     elif failure.check(DNSLookupError):
#     #         # this is the original request
#     #         request = failure.request
#     #         self.logger.error('DNSLookupError on %s', request.url)
#     #
#     #     # elif isinstance(failure.value, TimeoutError):
#     #     elif failure.check(TimeoutError):
#     #         request = failure.request
#     #         self.logger.error('TimeoutError on %s', request.url)
#     # headers = {
#     #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
#     # }
#     # def parse(self, response):
#     #     res = BeautifulSoup(response.body)
#     #     for news in res.select('.feature_news_r'):
#     #         print(news.text)
#     rules = [
#         Rule(LinkExtractor(allow=('page=[1-3]$')), callback='parse_list', follow=True)
#     ]
#     # def start_requests(self):
#     #     yield Request(url=self.login_page, callback=self.parse_httpbin, errback=self.errback_8891, dont_filter=True)
#     # def parse_httpbin(self, response):
#     #     self.logger.error('Got successful response from {}'.format(response.url))
#     #
#     # def errback_8891(self, failure):
#     #     # log all errback failures,
#     #     # in case you want to do something special for some errors,
#     #     # you may need the failure's type
#     #     self.logger.error(repr(failure))
#     #
#     #     # if isinstance(failure.value, HttpError):
#     #     if failure.check(HttpError):
#     #         # you can get the response
#     #         response = failure.value.response
#     #         self.logger.error('HttpError on %s', response.url)
#     #
#     #     # elif isinstance(failure.value, DNSLookupError):
#     #     elif failure.check(DNSLookupError):
#     #         # this is the original request
#     #         request = failure.request
#     #         self.logger.error('DNSLookupError on %s', request.url)
#     #
#     #     # elif isinstance(failure.value, TimeoutError):
#     #     elif failure.check(TimeoutError):
#     #         request = failure.request
#     #         self.logger.error('TimeoutError on %s', request.url)
#
#     def parse_list(self, response):
#         j_data = json.loads(response.text)
#         for j in j_data['data']['list']:
#             # print(j['link'])
#             yield scrapy.Request(j['link'], self.parse_detail)
#         # for news in j_data:
#         #     yield scrapy.Request(news.select('a')[0]['href'].split('/')[2], self.parse_detail)
#
#     def parse_detail(self, response):
#         res = BeautifulSoup(response.body)
#         einineitem = EinineItem()
#         einineitem['title'] = res.select('div.carTypDetail')[0].text.split('作者')[0].replace('\n', '')
#         einineitem['text'] = res.select('#article-box')[0].text
#         einineitem['time'] = res.select('.insidePageTime')[0].text
#         if len(einineitem['text']) > 0:
#             return einineitem
#         else:
#             return None