#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

# Scrapy settings for xueqiu project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

from common import beans

BOT_NAME = 'xueqiu'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
DEFAULT_REQUEST_HEADERS = {
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://xueqiu.com/hq',
    'Connection': 'keep-alive',
    'cache-control': 'no-cache',
    'DNT': '1',
}

SPIDER_MODULES = ['xueqiu.spiders']
NEWSPIDER_MODULE = 'xueqiu.spiders'

ITEM_PIPELINES = {
    'xueqiu.pipelines.CatelogFilterPipeline': 300,
}

FEED_FORMAT = 'csv'
FEED_URI = '%s/stock_symbol.csv' % beans['work_dir']
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
LOG_FILE = '%s/scrapy.log' % beans['work_dir']
LOG_STDOUT = True
