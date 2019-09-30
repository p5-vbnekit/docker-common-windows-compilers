#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, github

if "__main__" == __name__: from __main__ import __file__ as main_path

def routine():
  def make_release():
    m_old_name = sys.argv[1]
    if not m_old_name: raise ValueError("invalid old name")

    m_new_name = sys.argv[2]
    if not m_new_name: raise ValueError("invalid new name")
    if m_old_name == m_new_name: raise ValueError("invalid new name")

    m_token = sys.argv[3]
    if not m_token: m_token = None
    else m_token = os.environ[m_token]
  
    m_release = None
    for m_item in github.Github(m_token).get_releases()
      if m_old_name != m_item.tag_name: continue
      if m_release is None: m_release = m_item
      elif m_item.created_at < m_release.created_at: m_release = m_item

    if m_release is None: raise RuntimeError("release not found")
    return m_release

  make_release().update(name = m_new_name)

if "__main__" == __name__: routine()
