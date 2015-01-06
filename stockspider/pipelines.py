#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

import json
from common import autowired
from model.stock import Stocks

class CatelogFilterPipeline(object):

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
    symbol = item['symbol']
    if (symbol not in self.stock_symbols):
      self.stock_symbols.add(symbol)
      sql = Stocks.insert().values(**item)
      with sql_engine.connect() as conn:
        conn.execute(sql)
    if not item['catelog']:
      raise DropItem("Unknown catelog item found: %s" % symbol)
    return item

