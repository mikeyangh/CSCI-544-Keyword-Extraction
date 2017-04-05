import scrapy
import urllib


def download(url, file_name):
    set_new_ip()
    r = requests.get(url='http://icanhazip.com/',
                          proxies=http_proxy,
                          verify=False)
    ip = r.text

    while ip in ip_set:
        set_new_ip()
        ip = requests.get(url='http://icanhazip.com/',
                          proxies=http_proxy,
                          verify=False).text
    print ip
    try:
        r = requests.get(url, proxies=http_proxy, verify=False)
        print r.status_code
        while r.status_code != 200:
            r = requests.get(url, proxies=http_proxy, verify=False)
        ip_set.add(ip)
        with open(file_name, 'wb') as fh:
            fh.write(r.content)
    except:
        print 'download fails for PDF ' + file_name

class QuotesSpider(scrapy.Spider):
    name = "fcst_pdf"

    def start_requests(self):
        urls = [
        	# "http://fcst.ceaj.org/CN/volumn/volumn_1690.shtml"
            "http://fcst.ceaj.org/CN/volumn/current.shtml"
		]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        file_name = response.url.split("/")[-1]
        prefix = file_name.split(".")[-2]
        page = prefix.split("_")[-1]
        # filename = 'fcst-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

        pdf_urls = response.css('a::attr(href)').re(r'.*PDF.*')
        for pdf_url in pdf_urls:
            print "pdf_url: " + pdf_url
            pdf_url = str(pdf_url)
            pdf_id = pdf_url.split('=')[-1]
            pdf_url = 'http://fcst.ceaj.org/CN/article/downloadArticleFile.do?attachType=PDF&id=' + pdf_id
            fh = open('id_list.txt', 'a')
            fh.write(pdf_id)
            fh.write('\n')
            fh.close()
            # opener = urllib.URLopener()
            # opener.retrieve(pdf_url, './pdf/' + page + '_' + pdf_id + '.pdf')
            # download(pdf_url, './tor/' + page + '_' + pdf_id + '.pdf')

        last_page_anchor = response.css('a').re(r'.*btn_previous.*')[0]
        last_page_u = last_page_anchor.split('\"')[1]
        last_page = str(last_page_u)
        if last_page is not None:
            last_page = response.urljoin(last_page)
            yield scrapy.Request(last_page, callback=self.parse)