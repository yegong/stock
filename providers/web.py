#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

import logging
import traceback
import tornado.ioloop
import tornado.web
from common import inject

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Hello, world")

routes = [
  ('/', MainHandler),
]

class TornadoWeb:
  def __init__(self):
    self.application = tornado.web.Application(routes)
    self.ioloop = tornado.ioloop.IOLoop.instance()
    self._started = False
    self._stopped = False

  def start(self):
    if not self._started:
      self._started = True
      logging.info('Start web')
      self.application.listen(8080)
      self.ioloop.start()
    else:
      raise Exception('web has already started.')

  def stop(self):
    if not self._started:
      raise Exception('web not started.')
    elif self._stopped:
      raise Exception('web has already stopped')
    else:
      self._stopped = True
      self.ioloop.stop()

