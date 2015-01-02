#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

def chunks(l, n):
  """ Yield successive n-sized chunks from l.
  """
  for i in xrange(0, len(l), n):
    yield l[i:i+n]

