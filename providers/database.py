#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

from common import inject


@inject('database_url')
def engine(database_url):
  from sqlalchemy import create_engine
  return create_engine(database_url)

@inject('sql_engine')
def meta_data(sql_engine):
  from sqlalchemy import MetaData
  return MetaData(sql_engine)
