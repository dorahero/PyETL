import scrapy
from bs4 import BeautifulSoup
from playcar.items import PlaycarItem

class PlaycarCrawler(scrapy.Spider):
    name = 'playcar'
    # url = 'https://autos.udn.com/autos/ajax_article/{}/-1/7825?_={}'.format(p + 700, p + 700)
    start_urls = ['http://www.playcar.org/news.php?page={}&keyword_types='.format(p+1) for p in range(223)]
    def parse(self, response):
        domain = 'http://www.playcar.org/'
        soup = BeautifulSoup(response.body)
        for i, s in enumerate(soup.select('.container .blog-list a')):
            if i % 3 == 0:
                title = s.select('h4')[0].text
                time = s.select('span')[0].text
                yield scrapy.Request(url=domain + s['href'], callback=self.parse_detail, cb_kwargs={"title": title, "time": time})
    def parse_detail(self, response, title, time):
        res = BeautifulSoup(response.body)
        playcaritem = PlaycarItem()
        playcaritem['title'] = title
        playcaritem['text'] = res.select('div[class="post-entry clearfix"]')[0].text
        playcaritem['time'] = time
        if len(playcaritem['text']) > 0:
            return playcaritem
        return None