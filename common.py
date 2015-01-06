#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

assert __name__ != '__main__'

import logging.config

from utils.injection import *


logging.config.fileConfig('logging.conf')

appctx = ApplicationContextBuilder([
  ('database_url', value('mysql://python_dev:vao8Je1o@localhost/stock_dev')),
  ('working_dir', value('/Users/cooper/tmp/work')),
  ('sql_engine', factory_bean('providers.database.engine')),
  ('sql_meta_data', factory_bean('providers.database.meta_data')),
  ('spider_container', factory_bean('providers.spider.ScrapySpider')),
  ('web_container', factory_bean('providers.web.TornadoWeb')),
])
inject = appctx.injector()
autowired = appctx.auto_injector()
beans = appctx.beans

appctx.configure()
