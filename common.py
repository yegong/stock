#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

assert __name__ != '__main__'

import logging.config

from utils.injection import *


logging.config.fileConfig('logging.conf')

appctx = ApplicationContextBuilder([
  ('mysql_url', value('mysql://python_dev:vao8Je1o@localhost/stock_dev')),
  ('mongo_url', value('mongodb://localhost:27017/')),
  ('working_dir', value('/Users/cooper/tmp/work')),
  ('sql_engine', factory_bean('providers.database.sql_engine')),
  ('sql_meta_data', factory_bean('providers.database.sql_meta_data')),
  ('mongo_client', factory_bean('providers.database.mongo_client')),
  ('mongo_db', factory_bean('providers.database.mongo_db')),
  ('spider_container', factory_bean('providers.spider.ScrapySpider')),
  ('web_container', factory_bean('providers.web.TornadoWeb')),
])
inject = appctx.injector()
autowired = appctx.auto_injector()
beans = appctx.beans

appctx.configure()
