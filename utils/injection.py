#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

import inspect
import logging

from utils.decorator import private
from utils.collections import *
from functools import wraps


def value(val):
  """
  wrap a plain value for bean registration
  :type val: object
  """
  return 'value', val


def value_factory(val):
  """
  wrap a function to register it's return value as a bean
  :param val: function to generate bean
  :type val: function
  """
  return 'value_factory', val


def bean(val):
  """
  wrap a full qualified name of a object for bean registration
  :type val: str
  """
  return 'bean', val


def factory_bean(factory):
  """
  wrap a full qualified name of a function to register it's return value as a bean
  :type val: str
  """
  return 'factory_bean', factory

def depends_on(dependencies):
  if type(dependencies) == str:
    dependencies = [dependencies]
  def decorator(method):
    deps = []
    if (hasattr(method, '__injected_dependencies__')):
      deps = getattr(method, '__injected_dependencies__')
    deps += dependencies
    deps = list(set(deps))
    setattr(method, '__injected_dependencies__', deps)
    return method
  return decorator

class InjectionException(Exception):
  def __init__(self, message):
    self.message = message


class CycleDependencyException(InjectionException):
  def __init__(self, stack):
    self.stack = stack
    self.message = str(stack)


class ApplicationContextBuilder:
  def __init__(self, configurations):
    self.configurations = configurations
    self.bean_names = first(configurations)
    self.beans_map = dict()
    self.beans = lambda: None
    self.bean_configured = False

  def injector(self):
    """
    get a injection decorator with parameter
    :return: decorator function with parameter
    :rtype: function
    """
    def decorator_wrapper(*injections):
      not_found = [i for i in injections if i not in self.bean_names]
      if not_found:
          raise InjectionException('Dependencies not found: ' + str(not_found))

      def decorator(method):
        if not inspect.isfunction(method):
          raise InjectionException('Injection works on function only')

        @wraps(method)
        def decorated_method(*args, **kwargs):
          return self.invoke_injected_method(method, injections, *args, **kwargs)

        deps = list(injections)
        deps += getattr(method, '__injected_dependencies__', [])
        deps = list(set(deps))
        setattr(decorated_method, '__injected_dependencies__', deps)
        return decorated_method

      return decorator

    return decorator_wrapper

  def auto_injector(self):
    """
    get a `smart' injection decorator automatically inject parameters according to their names
    :return: decorator function
    :rtype function
    """

    def decorator(method):
      if not inspect.isfunction(method):
        raise InjectionException('Injection works on function only')
      arg_names = inspect.getargspec(method).args
      injections = [arg for arg in arg_names if arg in self.bean_names]

      @wraps(method)
      def decorated_method(*args, **kwargs):
        return self.invoke_injected_method(method, injections, *args, **kwargs)

      deps = injections
      deps += getattr(method, '__injected_dependencies__', [])
      deps = list(set(deps))
      setattr(decorated_method, '__injected_dependencies__', deps)
      return decorated_method

    return decorator

  @private
  def invoke_injected_method(self, injected_method, injections, *args, **kwargs):
    if not self.bean_configured:
      raise InjectionException('ApplicationContext is not configured yet')
    for name in injections:
      bean = self.beans_map[name]
      if bean is None:
        raise InjectionException('Dependency not found in runtime: ' + name)
      kwargs[name] = bean
    return injected_method(*args, **kwargs)

  def configure(self):
    """
    configure and startup
    """
    def do_configure():
      for bean_name, bean_configuration in self.configurations:
        create_bean(bean_name, bean_configuration, [])

    def create_bean(bean_name, bean_configuration, stack):
      if bean_name in self.beans_map:
        return
      if bean_name in stack:
        raise Exception("CycleDependencyException " + str(stack))
      stack.append(bean_name)
      bean = instantise(bean_name, bean_configuration, stack)
      self.beans_map[bean_name] = bean
      setattr(self.beans, bean_name, bean)
      stack.pop()

    def process_dependencies(bean_name, target, stack):
      for bean_name, bean_configuration in check_dependencies(bean_name, target):
        create_bean(bean_name, bean_configuration, stack)

    def check_dependencies(bean_name, target):
      deps = []
      deps += getattr(target, '__injected_dependencies__', [])
      if inspect.isclass(target) and hasattr(target, '__init__'):
        init_method = getattr(target, '__init__')
        deps += getattr(target.__init__, '__injected_dependencies__', [])
      if len(deps) > 0:
        logging.info('%s depends on %s' % (bean_name, ','.join(deps)))
      return [(bean_name, bean_configuration) for bean_name, bean_configuration in self.configurations if bean_name in deps]

    def instantise(bean_name, details, stack):
      def_type, value = details
      if def_type == 'value':
        logging.info('create %s' % bean_name)
        return value
      if def_type == 'value_factory':
        process_dependencies(bean_name, value, stack)
        logging.info('create %s' % bean_name)
        return value()
      target = get_target(value)
      if def_type == 'bean':
        logging.info('create %s' % bean_name)
        return target
      elif def_type == 'factory_bean':
        process_dependencies(bean_name, target, stack)
        logging.info('create %s' % bean_name)
        return target()
      raise InjectionException('Cannot instantise: ' + value)

    self.bean_configured = True
    do_configure()


@private
def get_target(fqn):
  fqn_parts = fqn.rsplit('.', 1)
  if len(fqn_parts) == 0:
    raise InjectionException('Unrecognized full qualified name: ' + fqn)
  target = None
  for name in fqn_parts:
    if target is None:
      target = __import__(name, None, None, [''])
    else:
      target = getattr(target, name)
      if target is None:
        raise InjectionException("Attribute '%s' is not found in '%s'" % (name, str(target)))
  return target
