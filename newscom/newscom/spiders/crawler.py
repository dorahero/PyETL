import scrapy
from bs4 import BeautifulSoup
from newscom.items import NewscomItem

class NewscomCrawler(scrapy.Spider):
    name = 'newscom'
    # url = 'https://autos.udn.com/autos/ajax_article/{}/-1/7825?_={}'.format(p + 700, p + 700)
    start_urls = ['https://www.carnews.com/article/category/a2eca5c1-a415-11e7-93e4-f4f26d026842?&page={}'.format(p+1) for p in range(2549)]
    def parse(self, response):
        domain = 'https://www.kingautos.net'
        soup = BeautifulSoup(response.body)
        for s in soup.select('#df-archive-content .article-title a'):
            title = s.text
            yield scrapy.Request(url=s['href'], callback=self.parse_detail, cb_kwargs={"title": title})
    def parse_detail(self, response, title):
        res = BeautifulSoup(response.body)
        newscomitem = NewscomItem()
        newscomitem['title'] = title
        newscomitem['text'] = res.select('#df-content-wrapper .entry-content')[0].text
        newscomitem['time'] = res.select('.vcard span')[0].text
        if len(newscomitem['text']) > 0:
            return newscomitem
        return None
