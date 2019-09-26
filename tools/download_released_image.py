#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
arguments: [yaml-style options string]

yaml-style options string:
  name: string, image file name; None or False or empty string for default; default is "chocolatey.tar"
  repo: string; None or False or empty string for default; default is "p5-vbnekit/docker-common-windows-compilers"
  release: string; None or False or empty string for default; default is latest
  token: string; can be None or False
  output: string, None or False or empty string for default; default is stdout
  verbose: boolean, None or False for default; default is True
  buffer_size: integer, None or False for default; default is 128 * 1024 * 1024
"""

import os, io, re, sys, yaml, ctypes, hashlib, github, urllib.request

if "__main__" == __name__: from __main__ import __file__ as main_path

def routine():
  def make_options():
    class Result(object):
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        m_arguments = sys.argv
        m_arguments_length = len(m_arguments)
        if 1 == m_arguments_length: m_dictionary = {}
        else:
          if 2 != m_arguments_length: raise ValueError("invalid command line: \"{} [yaml-style options string]\" expected".format(sys.argv[0]))
          with io.StringIO(sys.argv[1]) as m_stream: m_dictionary = yaml.load(m_stream)
        if not isinstance(m_dictionary, dict): raise TypeError("invalid options, dictionary expected")
        m_default_name = "chocolatey.tar"
        m_default_repo = "p5-vbnekit/docker-common-windows-compilers"
        m_default_release = None
        m_default_token = None
        m_default_output = None
        m_default_verbose = True
        m_default_buffer_size = 128 * 1024 * 1024
        if "name" in m_dictionary:
          self.__name = m_dictionary["name"]
          if not self.__name: self.__name = m_default_name
          elif not isinstance(self.__name, str): raise TypeError("invalid options, name: string expected")
        else: self.__name = m_default_name
        if "repo" in m_dictionary:
          self.__repo = m_dictionary["repo"]
          if not self.__repo: self.__repo = m_default_repo
          elif not isinstance(self.__repo, str): raise TypeError("invalid options, repo: string expected")
        else: self.__repo = m_default_repo
        if "release" in m_dictionary:
          self.__release = m_dictionary["release"]
          if not self.__release: self.__release = m_default_release
          elif not isinstance(self.__release, str): raise TypeError("invalid options, release: string expected")
        else: self.__release = m_default_release
        if "token" in m_dictionary:
          self.__token = m_dictionary["token"]
          if not self.__token: self.__token = m_default_token
          elif not isinstance(self.__token, str): raise TypeError("invalid options, token: string expected")
        else: self.__token = m_default_token
        if "output" in m_dictionary:
          self.__output = m_dictionary["output"]
          if not self.__output: self.__output = m_default_output
          elif not isinstance(self.__output, str): raise TypeError("invalid options, output: string expected")
        else: self.__output = m_default_output
        if "verbose" in m_dictionary:
          self.__verbose = m_dictionary["verbose"]
          if self.__verbose is None: self.__verbose = m_default_verbose
          elif not isinstance(self.__verbose, bool): raise TypeError("invalid options, verbose: boolean expected")
        else: self.__verbose = m_default_verbose
        if "buffer_size" in m_dictionary:
          self.__buffer_size = m_dictionary["buffer_size"]
          if self.__buffer_size is None: self.__buffer_size = m_default_buffer_size
          elif self.__buffer_size is False: self.__buffer_size = m_default_buffer_size
          else:
            if not isinstance(self.__buffer_size, int): raise TypeError("invalid options, buffer_size: positive integer expected")
            if not (0 < self.__buffer_size): raise ValueError("invalid options, buffer_size: positive integer expected")
        else: self.__buffer_size = m_default_buffer_size
      name = property(lambda self: self.__name)
      repo = property(lambda self: self.__repo)
      release = property(lambda self: self.__release)
      token = property(lambda self: self.__token)
      output = property(lambda self: self.__output)
      verbose = property(lambda self: self.__verbose)
      buffer_size = property(lambda self: self.__buffer_size)
    return Result()

  m_options = make_options()

  def make_log():
    if m_options.verbose:
      def routine(*args, **kwargs): return print(*args, **kwargs)
      return routine
    def routine(*args, **kwargs): pass
    return routine

  m_log = make_log()

  m_log("{}: name = \"{}\"".format(main_path, m_options.name), file = sys.stderr)
  m_log("{}: repo = \"{}\"".format(main_path, m_options.repo), file = sys.stderr)

  m_repo = github.Github(m_options.token).get_repo(m_options.repo)
  m_latest_release = m_repo.get_latest_release()

  def make_release():
    m_release = m_options.release
    if m_release is None: return m_latest_release
    return m_repo.get_release(m_release)

  m_release = make_release()

  m_log("{}: release = {}".format(main_path, "\"{}\"{}".format(m_release.tag_name, ", latest" if m_latest_release.id == m_release.id else "")), file = sys.stderr)
  m_log("{}: token = {}".format(main_path, "\"***\"" if m_options.token else None), file = sys.stderr)
  m_log("{}: output = {}".format(main_path, "\"{}\"".format(m_options.output) if m_options.output else "stdout"), file = sys.stderr)
  m_log("{}: verbose = {}".format(main_path, m_options.verbose), file = sys.stderr)
  m_log("{}: buffer_size = {}".format(main_path, m_options.buffer_size), file = sys.stderr)

  def make_assets():
    return { m_asset.name:m_asset for m_asset in m_release.get_assets() }

  m_assets = make_assets()

  def make_md5():
    m_txt = "{}.md5.txt"
    class Record(object):
      __hash_pattern = re.compile("^[0-9a-f]{32}$")
      __spacer_pattern = re.compile("^ [\\* ]$")
      __name_pattern = re.compile("^[^\\/]+$")
      def __init__(self, line):
        super().__init__()
        m_line = line.rstrip("\r\n")
        m_line_length = len(m_line)
        if not (34 < m_line_length): raise ValueError("invalid md5 line")
        self.__hash = m_line[:32]
        if self.__hash_pattern.match(self.__hash) is None: raise ValueError("invalid hash in md5 line")
        if self.__spacer_pattern.match(m_line[32:34]) is None: raise ValueError("invalid spacer in md5 line")
        self.__name = m_line[34:]
        if self.__name_pattern.match(self.__name) is None: raise ValueError("invalid name in md5 line")
        if m_txt == self.__name: raise ValueError("invalid name in md5 line")
      name = property(lambda self: self.__name)
      hash = property(lambda self: self.__hash)
    m_asset = m_assets["{}.md5.txt".format(m_options.name)]
    with urllib.request.urlopen(m_asset.browser_download_url) as m_response: return tuple([Record(m_line.decode("utf-8")) for m_line in m_response.readlines()])

  m_buffer = ctypes.create_string_buffer(m_options.buffer_size)

  def make_output():
    if m_options.output:
      class Result(object):
        def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.__path = str(m_options.output)
          self.__stream = open(m_options.output, "wb")
        @staticmethod
        def is_regular_file(): return True
        def write(self, data): return self.__stream.write(data)
        def flush(self): return self.__stream.flush()
        def close(self): return self.__close()
        def remove(self):
          m_path = self.__path
          self.__path = None
          if m_path: os.remove(m_path)
      return Result()
    class Result(object):
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      @staticmethod
      def is_regular_file(): return False
      @staticmethod
      def write(data): return sys.stdout.buffer.write(data)
      @staticmethod
      def flush(): return sys.stdout.flush()
    return Result()

  def do_cleanup_operation(operation):
    try: operation()
    except:
      try: traceback.print_exc(file = sys.stderr)
      except: pass

  m_output = make_output()

  try:
    def process_asset(md5_record):
      m_asset = m_assets[md5_record.name]
      m_log("{}: processing asset \"{}\", hash = \"{}\", url = \"{}\"".format(main_path, md5_record.name, md5_record.hash, m_asset.browser_download_url), file = sys.stderr)

      m_signature = hashlib.md5()
      with urllib.request.urlopen(m_asset.browser_download_url) as m_response:
        m_total = [0]
        def routine():
          m_size = m_response.readinto(m_buffer)
          if not (0 < m_size): return False
          m_signature.update(m_buffer[:m_size])
          m_total[0] += m_size
          m_log("{}: processing asset \"{}\" progress, size = \"{}\", url = \"{}\"".format(main_path, md5_record.name, m_total[0], m_asset.browser_download_url), file = sys.stderr)
          m_output.write(m_buffer[:m_size])
          m_output.flush()
          return True

        if not routine(): raise RuntimeError("unexpected EOF")
        while routine(): pass

        if md5_record.hash != m_signature.digest(): raise RuntimeError("hash mismatch")

    for m_md5_record in make_md5(): process_asset(m_md5_record)
    m_output.flush()

  except:
    if m_output.is_regular_file(): do_cleanup_operation(lambda: m_output.remove())
    raise

  finally:
    if m_output.is_regular_file(): do_cleanup_operation(lambda: m_output.close())

if "__main__" == __name__: routine()
