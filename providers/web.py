#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

import logging
import traceback
import tornado.ioloop
import tornado.web
import os
import mako.lookup
import mako.template
from common import autowired, depends_on

class MakoHandler(tornado.web.RequestHandler):
  def initialize(self):
    template_path = self.get_template_path()
    self.lookup = mako.lookup.TemplateLookup(directories=[template_path], input_encoding='utf-8', output_encoding='utf-8')

  def render_string(self, filename, **kwargs):
    template = self.lookup.get_template(filename)
    namespace = self.get_template_namespace()
    namespace.update(kwargs)
    return template.render(**namespace)

  def render(self, filename, **kwargs):
    self.finish(self.render_string(filename, **kwargs))

class MainHandler(MakoHandler):
  @autowired
  def get(self, sql_engine):
    with sql_engine.connect() as conn:
      from model.stock import Stocks
      count = conn.execute(Stocks.count()).first()
      self.render('index.html', title='Hello', body=str(count))

routes = [
  ('/', MainHandler),
]

settings = {
  'template_path' : os.path.join(os.path.dirname(__file__), '..', 'templates')
}

@depends_on('sql_engine')
class TornadoWeb:
  def __init__(self):
    self.application = tornado.web.Application(routes, **settings)
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

