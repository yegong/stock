#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

import logging.config

urls = (
  '/', 'yacai.web.controllers.index.Index',
)

if __name__ == '__main__':
  import common

  logging.config.fileConfig('logging.conf')
  assert common.appctx.bean_configured
  
  common.beans['spider'].start()

  import web
  app = web.application(urls, globals())
  app.run()
