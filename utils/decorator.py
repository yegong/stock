#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'


def private(something):
  """
  declear something is private
  """
  something.__private__ = True
  return something
