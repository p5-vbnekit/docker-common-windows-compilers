#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, sys

if "__main__" == __name__:
  from __main__ import __file__ as m_main_path
  m_begin = time.monotonic()
  while True:
    time.sleep(+2.0e+2)
    print("{}: this message had to be sent, otherwise travis-ci will stop the the deployment of large files by 10 minutes timeout, time elapsed: {} minutes...".format(m_main_path, (time.monotonic() - m_begin) / +6.0e+1), file = sys.stderr)
    sys.stderr.flush()
  print("{}: time elapsed: {} minutes, exiting...".format(m_main_path, (time.monotonic() - m_begin) / +6.0e+1), file = sys.stderr)
  sys.stderr.flush()
