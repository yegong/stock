#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'
import scrapy, json
from dateutil import parser
from scrapy import log
from scrapy.selector import Selector
import utils
from stockspider.items import *

class HqSpider(scrapy.Spider):
  name = "hq"
  allowed_domains = ["xueqiu.com"]
  access_token = None

  def start_requests(self):
    request_hq_access_token = scrapy.Request("http://xueqiu.com/hq", callback=self.parse_hq)
    return [request_hq_access_token]

  def parse_hq(self, response):
    access_token_list = response.xpath('//script').re('SNB.data.access_token.*\|\| "(.*)";')
    assert len(access_token_list) == 1
    self.access_token = access_token_list[0]
    request = scrapy.Request("http://xueqiu.com/stock/cata/stocklist.json?page=1&size=0&order=desc&orderby=percent&type=11%2C12&_=1", 
        cookies=self.get_cookies(),
        headers=self.get_ajax_header(),
        callback=self.parse_hq_count)
    return request

  def parse_hq_count(self, response):
    json_response = json.loads(response.body_as_unicode())
    count = int(json_response['count']['count'])
    page_size = 100
    for page in xrange(0, count / page_size + 1):
      request = scrapy.Request("http://xueqiu.com/stock/cata/stocklist.json?page=%d&size=%d&order=desc&orderby=percent&type=11%%2C12&_=1" % (page + 1, page_size), 
          cookies=self.get_cookies(),
          headers=self.get_ajax_header(),
          callback=self.parse_hq_stock_name_list)
      yield request

  def parse_hq_stock_name_list(self, response):
    json_response = json.loads(response.body_as_unicode())
    if 'success' not in json_response or json_response['success'] != 'true':
      log.msg('parse_hq_stock_name_list parse failed')
      return
    for stock in json_response['stocks']:
      item = StockItem()
      item['symbol'] = stock['symbol']
      item['name'] = stock['name']
      item['market'] = getmarket(stock['symbol'])
      item['catelog'] = getcatelog(stock['symbol'])
      yield item
      
      if item['market'] == 'PRE':
        continue

      request = scrapy.Request("http://xueqiu.com/S/%s" % stock['symbol'], 
          cookies=self.get_cookies(),
          callback=self.parse_hq_stock)
      yield request

      import datetime
      from dateutil.relativedelta import relativedelta
      now = datetime.datetime.now()
      years_ago = datetime.datetime.now() - relativedelta(years=1)
      datetime_to_timestamp = lambda dt: int((dt  - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
      begin = datetime_to_timestamp(years_ago)
      end = datetime_to_timestamp(now)
      request = scrapy.Request("http://xueqiu.com/stock/forchartk/stocklist.json?symbol=%s&period=1day&type=after&begin=%d&end=%d&_=1" % (stock['symbol'], begin, end), 
          cookies=self.get_cookies(),
          callback=self.parse_hq_stock_k_1d)
      yield request
    
  def parse_hq_stock(self, response):
    for td in response.xpath('//table[@class="topTable"]/tr/td').extract():
      td_selector = Selector(text=td)
      name_list = td_selector.xpath('//td/text()').extract()
      value_list = td_selector.xpath('//td/span/text()').extract()
      if len(name_list) and len(value_list):
        name = name_list[0]
        value = value_list[0]
        log.msg(name + '_' + value)

  def parse_hq_stock_k_1d(self, response):
    json_response = json.loads(response.body_as_unicode())
    if 'success' not in json_response or json_response['success'] != 'true':
      log.msg('parse_hq_stock_k_1d parse failed')
      return
    symbol = json_response['stock']['symbol']
    if json_response['chartlist']:
      for chart in json_response['chartlist']:
        item = StockKLineDayItem()
        item['symbol'] = symbol
        item['day'] = parser.parse(chart['time']).replace(tzinfo=None)
        item['open_price'] = chart['open']
        item['close_price'] = chart['close']
        item['low_price'] = chart['low']
        item['high_price'] = chart['high']
        item['delta_price'] = chart.get('chg', 0)
        item['turn_rate'] = chart.get('turnrate', 0)
        item['delta_percent'] = chart.get('percent', 0)
        item['ma5'] = chart.get('ma5', None)
        item['ma10'] = chart.get('ma10', None)
        item['ma20'] = chart.get('ma20', None)
        item['ma30'] = chart.get('ma30', None)
        item['volume'] = chart.get('volume', 0)
        yield item

  def get_ajax_header(self):
    return {'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest'}

  def get_cookies(self):
    return {'xq_a_token': self.access_token}

