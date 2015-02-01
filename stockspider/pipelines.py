#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

import json
from common import autowired
from model.stock import Stocks, StockKLineDays
from stockspider.items import *

class StockPipeline(object):

  @autowired
  def __init__(self, sql_engine):
    stocks = []
    sql = Stocks.select()
    with sql_engine.connect() as conn:
      stocks = list(conn.execute(sql))
    self.stock_symbols = set([s.symbol for s in stocks])
    pass

  @autowired
  def process_item(self, item, spider, sql_engine):
    if type(item) != StockItem:
      return
    symbol = item['symbol']
    if (symbol not in self.stock_symbols):
      self.stock_symbols.add(symbol)
      sql = Stocks.insert().values(**item)
      with sql_engine.connect() as conn:
        conn.execute(sql)
    return item

class StockKLineDayPipeline(object):

  @autowired
  def process_item(self, item, spider, sql_engine):
    if type(item) != StockKLineDayItem:
      return
    symbol = item['symbol']
    sql = StockKLineDays.insert(mysql_replace_into='').values(**item)
    with sql_engine.connect() as conn:
      conn.execute(sql)
    return item

