#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

assert __name__ != '__main__'

import logging.config

from utils.injection import *


logging.config.fileConfig('logging.conf')

appctx = ApplicationContextBuilder([
  ('database_url', value('mysql://yacai_dev:shaN7aNg@127.0.0.1/yacai_dev')),
  ('sql_engine', factory_bean('providers.database.engine')),
  ('sql_meta_data', factory_bean('providers.database.meta_data')),
  ('work_dir', value('/Users/cooper/tmp/work')),
  ('spider', factory_bean('providers.spider.SpiderCore')),
])
inject = appctx.injector()
autowired = appctx.auto_injector()
beans = appctx.beans

appctx.configure()
