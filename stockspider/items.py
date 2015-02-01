#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

def getmarket(symbol):
  for market in ['SH', 'SZ', 'PRE']:
    if symbol.startswith(market):
      return market
  return None

def getcatelog(symbol):
  catelogs = [
      ('SH00', '指数'),
      ('SH09', '质押'),
      ('SH10', '债券'),
      ('SH11', '转债'),
      ('SH60', 'A股'),
      ('SH50', '封基'),
      ('SH51', 'ETF'),
      ('SH90', 'B股'),
      ('SZ00', 'A股'),
      ('SZ15', 'ETF'),
      ('SZ16', 'LOF'),
      ('SZ18', '封基'),
      ('SZ20', 'B股'),
      ('SZ30', '创业板'),
      ('SZ39', '指数'),
      ('PRE', 'PRE'),
      ]
  for prefix, catelog in catelogs:
    if symbol.startswith(prefix):
      return catelog
  return None

class StockItem(scrapy.Item):
  name = scrapy.Field()
  symbol = scrapy.Field()
  market = scrapy.Field()
  catelog = scrapy.Field()

class StockKLineDayItem(scrapy.Item):
  symbol = scrapy.Field()
  day = scrapy.Field()
  open_price = scrapy.Field()
  close_price = scrapy.Field()
  low_price = scrapy.Field()
  high_price = scrapy.Field()
  delta_price = scrapy.Field()
  turn_rate = scrapy.Field()
  delta_percent = scrapy.Field()
  volume = scrapy.Field()
  ma5 = scrapy.Field()
  ma10 = scrapy.Field()
  ma20 = scrapy.Field()
  ma30 = scrapy.Field()
