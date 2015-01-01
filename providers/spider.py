#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

import traceback
from common import inject
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from xueqiu.spiders.hq_spider import HqSpider
from scrapy.utils.project import get_project_settings
from threading import Thread

class SpiderCore:
  def __init__(self):
    self.spider = HqSpider()
    self.crawler = crawler = Crawler(get_project_settings())
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(self.spider)
    crawler.start()
    log.start()
    def run():
      try:
        reactor.run()
      except Exception, e:
        print traceback.format_exc()
    self.thread = Thread(target=reactor.run, args=(False,))
    self.thread.start()

