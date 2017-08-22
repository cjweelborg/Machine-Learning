# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:33:40 2017

@author: Christian
"""

from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from webCrawler.items import WebcrawlerItem
from scrapy.http import Request
import re

class MySpider(BaseSpider):
    name = "webCrawler"
    allowed_domains = ['nomoregames.net']
    start_urls = ["https://www.nomoregames.net"]
    
    def parse(self, response):
        hxs = Selector(response)
        
        emails = hxs.xpath("//*[contains(text(),'@')]").extract()
        for email in emails:
            com = WebcrawlerItem()
            com["email"] = email
            com["location_url"] = response.url
            yield com
            
        forms = hxs.xpath('//form/@action').extract()
        for form in forms:
            formy = WebcrawlerItem()
            formy["form"] = form
            formy["location_url"] = response.url
            yield formy
            
#        comments = hxs.xpath('//comment()').extract()
#        for comment in comments:
#            com = WebcrawlerItem()
#            com["comments"] = comment
#            com["location_url"] = response.url
#            yield com
            
        visited_links = []
        links = hxs.xpath('//a/@href').extract()
        link_validator = re.compile("""^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.])(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$""")
        
        for link in links:
            if link_validator.match(link) and not link in visited_links:
                visited_links.append(link)
                yield Request(link, self.parse)
            else:
                full_url = response.urljoin(link)
                visited_links.append(full_url)
                yield Request(full_url, self.parse)