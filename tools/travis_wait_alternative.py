#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, subprocess, threading, time

if "__main__" == __name__:
  from __main__ import __file__ as m_main_path

  m_condition = True
  m_event = threading.Condition()

  def thread_routine():
    m_begin = time.monotonic()
    with m_event:
      while m_condition:
        if m_event.wait(+3.0e+2): continue
        if not m_condition: break
        print("{}: time elapsed: {}".format(m_main_path, time.monotonic() - m_begin), file = sys.stderr)
        sys.stderr.flush()
      print("{}: exiting".format(m_main_path), file = sys.stderr)
      sys.stderr.flush()

  m_command = sys.argv[1:]

  m_thread = threading.Thread(target = thread_routine, daemon = False)
  m_thread.start()

  try:
    m_process = subprocess.Popen(m_command, stderr = subprocess.PIPE)

    def thread_routine():
      for m_line in m_process.stderr:
        with m_event:
          sys.stderr.write(m_line.decode())
          sys.stderr.flush()
          m_event.notify_all()

    m_thread = threading.Thread(target = thread_routine, daemon = False)
    m_thread.start()
    m_process.wait()
    m_thread.join()
    m_result = m_process.returncode
    if 0 != m_result: raise RuntimeError("non-zero return code: {}".format(m_result))

  finally:
    with m_event:
      m_condition = False
      m_event.notify_all()
    m_thread.join()
