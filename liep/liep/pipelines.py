# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json


class LiepPipeline(object):
    def __init__(self):
        self.file = open('liepin.json','w')

    def process_item(self, item, spider):
        text = json.dumps(dict(item),ensure_ascii=False)
        self.file.write(text.encode('utf-8'))
        print 'QAQ ----> 正在写入数据'

    def close(self):
        self.file.close()
