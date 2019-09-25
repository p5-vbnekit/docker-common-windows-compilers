#!/bin/se -e

m_basename="$1"
test -n "${m_basename}"

for m_line in $(wget -O - "https://github.com/p5-vbnekit/docker-common-windows-compilers/releases/download/${TRAVIS_TAG}/${m_basename}.tar.md5.txt"); do
  m_md5=$(echo "${m_line}" | sed -re 's/^([^\s]+)  .+$/\1/')
  m_part=$(echo "${m_line}" | sed -re 's/^[^\s]+  (.+)$/\1/')
  wget -O "${m_part}" "https://github.com/p5-vbnekit/docker-common-windows-compilers/releases/download/${TRAVIS_TAG}/${m_part}"
  echo "${m_line}" | md5sum - c - 1>&2
  cat ${m_part}
  rm ${m_part}
done
