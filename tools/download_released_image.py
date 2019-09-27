#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
arguments: [yaml-dict-style options]

yaml-dict-style options string:
  name: string, image file name; None or False or empty string for default; default is "chocolatey.tar"
  repo: string; None or False or empty string for default; default is "p5-vbnekit/docker-common-windows-compilers"
  release: string; None or False or empty string for default; default is latest
  token: string; can be None or False
  output: string, None or False or empty string for default; default is stdout
  verbose: boolean, None or False for default; default is True
  buffer_size: positive integer > 0, None or False for default; default is 128 * 1024 * 1024
"""

import os, io, re, sys, yaml, time, ctypes, hashlib, github, traceback, urllib.request

if "__main__" == __name__: from __main__ import __file__ as main_path

def routine():
  def make_options():
    class Result(object):
      def __init__(self, name = None, repo = None, release = None, token = None, output = None, verbose = None, buffer_size = None):
        super().__init__()

        m_default_name = "chocolatey.tar"
        m_default_repo = "p5-vbnekit/docker-common-windows-compilers"
        m_default_release = None
        m_default_token = None
        m_default_output = None
        m_default_verbose = True
        m_default_buffer_size = 128 * 1024 * 1024

        self.__name = name
        if self.__name is None: self.__name = m_default_name
        elif self.__name is False: self.__name = m_default_name
        elif not isinstance(self.__name, str): raise TypeError("invalid options, name: string expected")
        elif not (0 < len(self.__name)): self.__name = m_default_name

        self.__repo = repo
        if self.__repo is None: self.__repo = m_default_repo
        elif self.__repo is False: self.__repo = m_default_repo
        elif not isinstance(self.__repo, str): raise TypeError("invalid options, repo: string expected")
        elif not (0 < len(self.__repo)): self.__repo = m_default_repo

        self.__release = release
        if self.__release is None: pass
        elif self.__release is False: self.__release = m_default_release
        elif not isinstance(self.__release, str): raise TypeError("invalid options, release: string expected")
        elif not (0 < len(self.__release)): self.__release = m_default_release

        self.__token = token
        if self.__token is None: pass
        elif self.__token is False: self.__token = m_default_token
        elif not isinstance(self.__token, str): raise TypeError("invalid options, token: string expected")
        elif not (0 < len(self.__token)): self.__token = m_default_token

        self.__output = output
        if self.__output is None: pass
        elif self.__output is False: self.__output = m_default_output
        elif not isinstance(self.__output, str): raise TypeError("invalid options, output: string expected")
        elif not (0 < len(self.__output)): self.__output = m_default_output

        self.__verbose = verbose
        if self.__verbose is None: self.__verbose = m_default_verbose
        elif not isinstance(self.__verbose, bool): raise TypeError("invalid options, verbose: boolean expected")

        self.__buffer_size = buffer_size
        if self.__buffer_size is None: self.__buffer_size = m_default_buffer_size
        elif self.__buffer_size is False: self.__buffer_size = m_default_buffer_size
        elif not isinstance(self.__buffer_size, int): raise TypeError("invalid options, buffer_size: positive integer > 0 expected")
        elif not (0 < self.__buffer_size): raise ValueError("invalid options, buffer_size: positive integer expected")

      name = property(lambda self: self.__name)
      repo = property(lambda self: self.__repo)
      release = property(lambda self: self.__release)
      token = property(lambda self: self.__token)
      output = property(lambda self: self.__output)
      verbose = property(lambda self: self.__verbose)
      buffer_size = property(lambda self: self.__buffer_size)

    def make_dictionary(arguments):
      m_result = {}
      m_argument_id = 0
      for m_argument in arguments:
        m_argument_id += 1
        m_argument = m_argument.strip("\r\n\t ")
        if not (0 < len(m_argument)): continue
        with io.StringIO(m_argument) as m_stream: m_loaded = yaml.load(m_stream)
        if not isinstance(m_loaded, dict): raise TypeError("invalid argument #{}, yaml-dict-style expected".format(m_argument_id))
        for m_key, m_value in m_loaded.items():
          if m_key in m_result: raise ValueError("invalid argument #{}, key \"{}\" dupplicate detected".format(m_argument_id, m_key))
          m_result[m_key] = m_value
      return m_result

    return Result(**make_dictionary(sys.argv[1:]))

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
      __digest_pattern = re.compile("^[0-9a-f]{32}$")
      __spacer_pattern = re.compile("^ [\\* ]$")
      __name_pattern = re.compile("^[^\\/]+$")
      def __init__(self, line):
        super().__init__()
        m_line = line.rstrip("\r\n")
        m_line_length = len(m_line)
        if not (34 < m_line_length): raise ValueError("invalid md5 line")
        self.__digest = m_line[:32]
        if self.__digest_pattern.match(self.__digest) is None: raise ValueError("invalid digest in md5 line")
        if self.__spacer_pattern.match(m_line[32:34]) is None: raise ValueError("invalid spacer in md5 line")
        self.__name = m_line[34:]
        if self.__name_pattern.match(self.__name) is None: raise ValueError("invalid name in md5 line")
        if m_txt == self.__name: raise ValueError("invalid name in md5 line")
      name = property(lambda self: self.__name)
      digest = property(lambda self: self.__digest)
    m_asset = m_assets["{}.md5.txt".format(m_options.name)]
    with urllib.request.urlopen(m_asset.browser_download_url) as m_response: return tuple([Record(m_line.decode("utf-8")) for m_line in m_response.readlines()])

  m_buffer = ctypes.create_string_buffer(m_options.buffer_size)
  m_buffer_length = len(m_buffer)

  def make_output():
    if m_options.output:
      class Result(object):
        def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.__path = str(m_options.output)
          self.__stream = open(m_options.output, "wb")
        @staticmethod
        def is_regular_file(): return True
        def seek(self, offset): return self.__stream.seek(offset, io.SEEK_SET)
        def write(self, data): return self.__stream.write(data)
        def flush(self): return self.__stream.flush()
        def close(self): return self.__stream.close()
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
      if not (0 < m_asset.size): return

      def make_md5(): return hashlib.md5()

      def make_context():
        class Result(object):
          def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.offset = 0
            self.md5 = make_md5()
        return Result()

      m_context = make_context()

      def make_input():
        def routine():
          m_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}
          if (0 < m_context.offset): m_headers["Range"] = "bytes={}-".format(m_context.offset)
          return urllib.request.urlopen(urllib.request.Request(url = m_asset.browser_download_url, headers = m_headers))
        m_try_number = 0
        while True:
          m_try_number += 1
          m_log("{}: opening url, try #{}, asset = \"{}\", url = \"{}\"".format(main_path, m_try_number, md5_record.name, m_asset.browser_download_url), file = sys.stderr)
          try: return routine()
          except OSError:
            traceback.print_exc(file = sys.stderr)
            if not (3 > m_try_number): raise
          except: raise
          m_log("{}: waiting 5 seconds".format(main_path), file = sys.stderr)
          time.sleep(+5.0e+0)

      def routine(try_number):
        with make_input() as m_input:
          def routine():
            try: m_size = m_input.readinto(m_buffer)
            except (OSError):
              if not (3 > try_number): raise
              traceback.print_exc(file = sys.stderr)
              return False
            try:
              if not (0 < m_size): raise RuntimeError("unexpected EOF")
              m_expected = min(m_asset.size - m_context.offset, m_buffer_length)
              if not (m_size <= m_expected): raise OverflowError("unexpected data")
            except:
              if not (3 > try_number): raise
              traceback.print_exc(file = sys.stderr)
              return False
            if m_size != m_output.write(m_buffer[:m_size]): raise RuntimeError("failed to write")
            m_output.flush()
            m_context.md5.update(m_buffer[:m_size])
            m_context.offset += m_size
            return True
          while m_context.offset < m_asset.size:
            if not routine(): return False

        try:
          m_md5_digest = m_context.md5.hexdigest()
          m_log("{}: asset \"{}\" was processed, size = {}, md5 = \"{}\"".format(main_path, md5_record.name, m_context.offset, m_md5_digest), file = sys.stderr)
          if m_asset.size != m_context.offset: raise RuntimeError("size mismatch")
          if md5_record.digest != m_md5_digest: raise RuntimeError("md5 mismatch")
        except:
          if not m_output.is_regular_file(): raise
          if not (3 > try_number): raise
          try:
            m_output.seek(0)
            m_output.truncate(0)
            m_context.md5 = make_md5()
            traceback.print_exc(file = sys.stderr)
            return False
          except: traceback.print_exc(file = sys.stderr)
          raise
        return True

      m_try_number = 0
      while True:
        m_try_number += 1
        m_log("{}: processing asset \"{}\", try #{}, expected size = {}, expected md5 = \"{}\"".format(main_path, md5_record.name, m_try_number, m_asset.size, md5_record.digest), file = sys.stderr)
        if routine(m_try_number): break
        m_log("{}: waiting 5 seconds".format(main_path), file = sys.stderr)
        time.sleep(+5.0e+0)

    for m_md5_record in make_md5(): process_asset(m_md5_record)
    m_output.flush()

  except:
    if m_output.is_regular_file(): do_cleanup_operation(lambda: m_output.remove())
    raise

  finally:
    if m_output.is_regular_file(): do_cleanup_operation(lambda: m_output.close())

if "__main__" == __name__: routine()
