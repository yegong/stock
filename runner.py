#!/usr/bin/env python
# -*- coding: utf8 -*-
import common
__author__ = 'cooper'

urls = (
  '/', 'yacai.web.controllers.index.Index',
)

if __name__ == '__main__':
  assert common.appctx.bean_configured
  import web
  app = web.application(urls, globals())
  app.run()
