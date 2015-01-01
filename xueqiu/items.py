# -*- coding: utf-8 -*-

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

class StockSymbolItem(scrapy.Item):
  name = scrapy.Field()
  symbol = scrapy.Field()
  market = scrapy.Field()
  catelog = scrapy.Field()
