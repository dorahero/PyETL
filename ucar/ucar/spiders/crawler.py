import scrapy
from bs4 import BeautifulSoup
from ucar.items import UcarItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_selenium import SeleniumRequest

class UcarCrawler(CrawlSpider):
    name = 'ucar'
    start_urls = ['https://news.u-car.com.tw/article?keywords=']
    # def parse(self, response):
    #     res = BeautifulSoup(response.body)
    #     for news in res.select('.feature_news_r'):
    #         print(news.text)
    rules = [
        Rule(LinkExtractor(allow=('&page=[1-9]$')), callback='parse_list', follow=True)
    ]

    def parse_list(self, response):
        domain = 'https://news.u-car.com.tw/article/'
        res = BeautifulSoup(response.body)
        for news in res.select('.feature_news_r'):
            yield scrapy.Request(domain + news.select('a')[0]['href'].split('/')[2], self.parse_detail)

    def parse_detail(self, response):
        res = BeautifulSoup(response.body)
        ucaritem = UcarItem()
        ucaritem['title'] = res.select('.title_area')[0].select('.title')[0].text
        ucaritem['text'] = res.select('.postcont')[0].text.split('\n\n\n\n\n\n\n\n\n')[0]
        ucaritem['time'] = str(str(res.select('.title_area')[0].select('.year_area')[0].text) + '年' + \
                           str(res.select('.title_area')[0].select('.month_area')[0].text) + \
                           str(res.select('.title_area')[0].select('.date_area')[0].text) + '日').replace('\n', '')
        return ucaritem




