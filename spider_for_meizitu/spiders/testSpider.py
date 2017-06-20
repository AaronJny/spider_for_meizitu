#coding=utf-8
import scrapy
from scrapy.http import Request,HtmlResponse
import os
import urllib
from scrapy.selector import Selector

class TestSpider(scrapy.spiders.Spider):
    name='meizitu'
    allowed_domians=["meizitu.com"]
    start_urls=['http://www.meizitu.com/a/',]
    for i in range(2,91):
        start_urls.append('http://www.meizitu.com/a/list_1_'+str(i)+'.html')
    print start_urls
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'www.meizitu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3013.3 Safari/537.36'
    }

    # def start_requests(self):
    #     return [Request('http://www.meizitu.com/a/',headers=self.headers,callback=self.parse)]

    def make_requests_from_url(self,url):
        return Request(url, headers=self.headers,dont_filter=True)

    def parse3(self,response):
        file_path=response.meta['file_path']
        with open(file_path,'wb') as f:
            f.write(response.body)

    def parse2(self,response):
        src_links=response.xpath('//img[re:test(@src,"http://mm.howkuai.com/wp-content/uploads/20\d{2}a/\d{2}/\d{2}/\d+.jpg")]/@src').extract()
        base_path=os.path.join("image",response.xpath('//div[contains(@class,"metaRight")]/h2/a/text()').extract()[0])
        header={
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3013.3 Safari/537.36'
        }
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        for i in range(len(src_links)):
            file_path = os.path.join(base_path, str(i)+'.jpg')
            yield Request(src_links[i],meta={'file_path':file_path},headers=header,callback=self.parse3)
        links = response.xpath('//a[re:test(@href,"http://www.meizitu.com/a/\d+.html")]/@href').extract()
        print links
        for url in links:
            yield Request(url, headers=self.headers, callback=self.parse2)

    def parse(self,response):
        current_url=response.url
        # unicode_body=response.body_as_unicode()
        print current_url
        # print unicode_body
        # print response.status
        links=response.xpath('//a[re:test(@href,"http://www.meizitu.com/a/\d+.html")]/@href').extract()
        print links
        for url in links:
            yield Request(url,headers=self.headers,callback=self.parse2)