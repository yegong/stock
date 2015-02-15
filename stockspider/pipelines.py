#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

import json
from common import autowired
from stockspider.items import *
from scrapy import log

class StockPipeline(object):

  @autowired
  def process_item(self, item, spider, mongo_db):
    if type(item) != StockItem:
      return item
    mongo_db.stocks.update({'symbol': item['symbol']}, {"$set": dict(item)}, upsert=True)
    return item

class StockKLineDayPipeline(object):

  @autowired
  def process_item(self, item, spider, mongo_db):
    if type(item) != StockKLineDayItem:
      return item
    #symbol = item['symbol']
    #sql = StockKLineDays.insert(mysql_replace_into='').values(**item)
    #with sql_engine.connect() as conn:
    #  conn.execute(sql)
    return item

