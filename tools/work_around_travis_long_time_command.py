#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, subprocess, threading, time

if "__main__" == __name__:
  from __main__ import __file__ as m_main_path

  def make_context():
    class Result(object):
      event = property(lambda self: self.__event)
      wait_duration = property(lambda self: self.__wait_duration)
      initial_time_point = property(lambda self: self.__initial_time_point)
      __wait_duration = +3.0e+0
      __initial_time_point = time.monotonic()
      def __init__(self):
        super().__init__()
        self.stop_flag = False
        self.__event = threading.Condition()
        self.last_time_point = self.__initial_time_point
        self.barrier_time_point = self.last_time_point + self.wait_duration
    return Result()

  m_context = make_context()

  def thread_routine():
    m_message_template = "{}: this message had to be sent, otherwise travis-ci will stop the job by 10 minutes timeout, child process stderr is already silent for {} minutes, total time elapsed: {} minutes..."
    with m_context.event:
      def wait_barrier(current_time_point):
        m_duration = m_context.barrier_time_point - current_time_point
        if not (+0.0e+0 < m_duration): return False
        m_context.event.wait(max(+1.0e-2, m_duration))
        return True
      while not m_context.stop_flag:
        m_current_time_point = time.monotonic()
        if wait_barrier(m_current_time_point): continue
        m_context.barrier_time_point = m_current_time_point + m_context.wait_duration
        print(m_message_template.format(m_main_path, (m_current_time_point - m_context.last_time_point) / +6.0e+1, (m_current_time_point - m_context.initial_time_point) / +6.0e+1, file = sys.stderr))
        sys.stderr.flush()
      print("{}: exiting".format(m_main_path), file = sys.stderr)
      sys.stderr.flush()

  m_command = sys.argv[1:]

  m_thread = threading.Thread(target = thread_routine, daemon = False)
  m_thread.start()

  try:
    m_process = subprocess.Popen(m_command, stderr = subprocess.PIPE)

    for m_line in m_process.stderr:
      with m_context.event:
        sys.stderr.buffer.write(m_line)
        sys.stderr.flush()
        m_context.last_time_point = time.monotonic()
        m_context.barrier_time_point = m_context.last_time_point + m_context.wait_duration
        m_context.event.notify_all()

    m_process.wait()
    m_result = m_process.returncode
    if 0 != m_result: raise RuntimeError("non-zero return code: {}".format(m_result))

  finally:
    with m_context.event:
      m_context.stop_flag = True
      m_context.event.notify_all()
    m_thread.join()
