#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-1-2

@author: Xu
"""
from scrapy import cmdline  #引入命令行
cmdline.execute('scrapy crawl lp'.split())