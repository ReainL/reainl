# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from liep.items import LiepItem
import re

class LpSpider(CrawlSpider):
    reg = re.compile('\s*')
    name = 'lp'
    allowed_domains = ['www.liepin.com']
    start_urls = ['https://www.liepin.com/zhaopin/?pubTime=&ckid=6f6956c5d999c17e&fromSearchBtn=2&compkind=&isAnalysis=&init=-1&searchType=1&dqs=020&industryType=&jobKind=&sortFlag=15&degradeFlag=0&industries=040&salary=0%240&compscale=&key=python&clean_condition=&headckid=7a006343bdb04f47&curPage=0',]

    #定义提取超链接的提取规则
    page_link = LinkExtractor(allow=('&curPage=\d+'))
    #定义爬取数据的规则
    rules = {
        Rule(page_link,callback='parse_content',follow=True)

    }

    #定义处理函数
    def parse_content(self, response):
        #定义一个Item,用于存储数据
        item = LiepItem()
        #获取整个我们需要的数据区域
        job_list = response.xpath('//div[@class="job-info"]')
        for job in job_list:
            name = job.xpath('.//h3/a')
            item['name'] = self.reg.sub('', name.xpath('string(.)').extract()[0])
            item['company'] = job.xpath('..//p[@class="company-name"]/a/text()').extract()
            item['salary'] = job.xpath('.//span[@class="text-warning"]/text()').extract()
            item['address'] = job.xpath('.//p[@class="condition clearfix"]//a/text()').extract()
            item['experience'] = job.xpath('.//p[@class="condition clearfix"]//span[3]/text()').extract()

            yield item
