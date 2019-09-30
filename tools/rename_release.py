#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, github, requests, json

if "__main__" == __name__: from __main__ import __file__ as main_path

def routine():
  if 4 != len(sys.argv): raise ValueError("invalid command line")
    
  m_old_name = sys.argv[1]
  if not m_old_name: raise ValueError("invalid old name")

  m_new_name = sys.argv[2]
  if not m_new_name: raise ValueError("invalid new name")
  if m_old_name == m_new_name: raise ValueError("invalid new name")

  m_token = sys.argv[3]
  if not m_token: m_token = None
  else: m_token = os.environ[m_token]

  def make_request_url():
    m_release = None
    m_repository = github.Github(m_token).get_repo("p5-vbnekit/docker-common-windows-compilers")
    for m_item in m_repository.get_releases():
      if m_old_name != m_item.tag_name: continue
      if m_release is None: m_release = m_item
      elif m_item.created_at < m_release.created_at: m_release = m_item

    if m_release is None: raise RuntimeError("release not found")
    return m_release.url

  def make_request_options():
    m_result = {
      "data": json.dumps({"name": m_new_name, "tag_name": m_new_name})
    }
    if not (m_token is None): m_result["auth"] = (m_token, "")
    return m_result

  m_result = requests.patch(make_request_url(), **make_request_options())
  if 200 != m_result.status_code: raise RuntimeError(str(m_result.text))

if "__main__" == __name__: routine()
