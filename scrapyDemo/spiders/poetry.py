# -*- coding: utf-8 -*-
import scrapy
import re


class PoetrySpider(scrapy.Spider):
    name = 'poetry'
    allowed_domains = ['so.gushiwen.org']
    start_urls = ['https://so.gushiwen.org/gushi/tangshi.aspx']


    def parse(self, response):
        url = "https://so.gushiwen.org"
        for href in response.css('div.typecont a::attr(href)').extract():
            yield scrapy.Request(url + href, callback=self.parse_category)

    def parse_category(self, response):
        poetryDict = {}
        title = response.css('h1::text').extract()[0]
        year = response.css('a[href*="cstr"]::text').extract()[0]
        author = response.css('a[href*="authorv"]::text').extract()[0]
        patternContent = re.compile(r'class="contson".*?>(.*?)</div>', re.S)
        #被<br/>打断
        #print("内容："+response.css('div.contson::text').extract()[0])
        content = re.search(patternContent, response.text).group(1).replace("<br />", "\n")
        poetryDict['title'] = title
        poetryDict['year'] = year
        poetryDict['author'] = author
        poetryDict['content'] = content
        yield poetryDict