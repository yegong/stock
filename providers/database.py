#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

from common import inject


@inject('mysql_url')
def sql_engine(mysql_url):
  from sqlalchemy import create_engine
  return create_engine(mysql_url)

@inject('sql_engine')
def sql_meta_data(sql_engine):
  from sqlalchemy import MetaData
  return MetaData(sql_engine)

@inject('mongo_url')
def mongo_client(mongo_url):
  from pymongo import MongoClient
  return MongoClient(mongo_url)

@inject('mongo_client')
def mongo_db(mongo_client):
  return mongo_client['stock_dev']

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert

@compiles(Insert, 'mysql')
def replace_into(insert, compiler, **kw):
  s = compiler.visit_insert(insert, **kw)
  s = s.replace("INSERT INTO", "REPLACE INTO")
  return s

Insert.argument_for("mysql", "replace_into", None)
