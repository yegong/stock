#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'
import scrapy, json
import utils
from xueqiu.items import *

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
    results = []
    if (json_response['success'] == 'true'):
      for stock in json_response['stocks']:
        item = StockSymbolItem()
        item['symbol'] = stock['symbol']
        item['name'] = stock['name']
        item['market'] = getmarket(stock['symbol'])
        item['catelog'] = getcatelog(stock['symbol'])
        request = scrapy.Request("http://xueqiu.com/S/%s" % stock['symbol'], 
            cookies=self.get_cookies(),
            callback=self.parse_hq_stock)
        #yield request
        yield item
    
  def parse_hq_stock(self, response):
    for tr in response.xpath('//table[@class="topTable"]/tr/td'):
      print tr

  def get_ajax_header(self):
    return {'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest'}

  def get_cookies(self):
    return {'xq_a_token': self.access_token}

