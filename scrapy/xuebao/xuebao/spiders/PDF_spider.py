import scrapy
import urllib

domain = 'http://cjc.ict.ac.cn'

class QuotesSpider(scrapy.Spider):
    name = "xuebao"

    def start_requests(self):
        urls = []
        for i in range(4699, 5000):
            urls.append('http://cjc.ict.ac.cn/qwjs/view.asp?id=' + str(i))	
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.status != 200:
            print 'Page downloading fails'
            return
        page_id = response.url.split('=')[-1]
        url = response.css('a::attr(href)').extract_first()
        url = domain + str(url)
        print url
        opener = urllib.URLopener()
        opener.retrieve(url, './pdf/' + page_id + '.pdf')
        #except:
        #    print 'Exception parsing page ' + page_id 
