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

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert

@compiles(Insert, 'mysql')
def replace_into(insert, compiler, **kw):
  s = compiler.visit_insert(insert, **kw)
  s = s.replace("INSERT INTO", "REPLACE INTO")
  return s

Insert.argument_for("mysql", "replace_into", None)
