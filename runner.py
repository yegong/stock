#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'cooper'

import logging.config


if __name__ == '__main__':
  import common
  logging.config.fileConfig('logging.conf')
  assert common.appctx.bean_configured
  

  import signal
  import sys
  def signal_handler(signal, frame):
    logging.info('Stop spider')
    common.beans.spider_container.stop()
    logging.info('Stop web')
    common.beans.web_container.stop()
    logging.info('Exit')
    sys.exit(0)
  signal.signal(signal.SIGINT, signal_handler)

  common.beans.spider_container.start() #async
  common.beans.web_container.start() #sync
  

