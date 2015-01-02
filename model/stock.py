#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

from sqlalchemy import Table
from common import beans

_sql_meta_data = beans['sql_meta_data']
_sql_engine = beans['sql_engine']
stocks = Table('stocks', _sql_meta_data, autoload=True, autoload_with=_sql_engine)
