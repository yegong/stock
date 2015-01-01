#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

from jinja2 import Environment, FileSystemLoader

from common import autowired


@autowired
def jinja_render(render_path):
  def json_default(val):
    import inspect
    if inspect.isclass(val):
      return val.__name__
    else:
      return val.__dict__

  def json(val):
    import simplejson as json
    return json.dumps(val, default=json_default, namedtuple_as_object=True, indent=__debug__)

  class JinjaRender:
    def __init__(self, render_path):
      loader = FileSystemLoader(render_path)
      env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)
      env.filters['json'] = json
      self.jinja_environment = env

    def __getattr__(self, name):
      path = name + '.html'
      t = self.jinja_environment.get_template(path)
      return t.render

  return JinjaRender(render_path)
