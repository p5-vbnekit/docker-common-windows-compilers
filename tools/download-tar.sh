#!/bin/se -e

m_base_url="$1"
test -n "${m_base_url}"

m_base_name="$2"
test -n "${m_base_name}"

for m_line in $(wget -O - "${m_base_url}/${m_base_name}.tar.md5.txt"); do
  m_md5=$(echo "${m_line}" | sed -re 's/^([^\s]+)  .+$/\1/')
  m_part=$(echo "${m_line}" | sed -re 's/^[^\s]+  (.+)$/\1/')
  wget -O "${m_part}" "${m_base_url}/${m_part}"
  echo "${m_line}" | md5sum - c - 1>&2
  cat ${m_part}
  rm ${m_part}
done
