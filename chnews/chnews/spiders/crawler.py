import scrapy
from bs4 import BeautifulSoup
from chnews.items import ChnewsItem

class ChnewsCrawler(scrapy.Spider):
    name = 'chnews'
    # url = 'https://autos.udn.com/autos/ajax_article/{}/-1/7825?_={}'.format(p + 700, p + 700)
    start_urls = ['https://want-car.chinatimes.com/news/?page={}'.format(p+1) for p in range(1623)]
    def parse(self, response):
        domain = 'https://want-car.chinatimes.com/'
        soup = BeautifulSoup(response.body)
        for s in soup.select('.news-list ul h3 a'):
            title = s.text
            yield scrapy.Request(url=domain + s['href'], callback=self.parse_detail, cb_kwargs={"title": title})
    def parse_detail(self, response, title):
        res = BeautifulSoup(response.body)
        chnewsitem = ChnewsItem()
        chnewsitem['title'] = title
        chnewsitem['text'] = res.select('article article')[0].text
        chnewsitem['time'] = res.select('.reporter time')[0].text
        if len(chnewsitem['text']) > 0:
            return chnewsitem
        return None