#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

import operator

first = lambda items: map(operator.itemgetter(0), items)
second = lambda items: map(operator.itemgetter(1), items)
zip_with_index = lambda items: zip(items, xrange(len(items)))


def filter_at(idx, predicate, items):
  return [item for item in items if predicate(item[idx])]