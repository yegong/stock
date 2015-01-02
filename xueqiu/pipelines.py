#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class CatelogFilterPipeline(object):
  def __init__(self):
    pass

  def process_item(self, item, spider):
    symbol = item['symbol']
    if not item['catelog']:
      raise DropItem("Unknown catelog item found: %s" % symbol)
    return item

