#!/bin/se -e

export m_base_url="$1"
test -n "${m_base_url}"

export m_base_name="$2"
test -n "${m_base_name}"

routine1() {
  wget -O "$3" "${1}/${3}" && (echo "$2" | md5sum -c - 1>&2) && cat "$3"
}

routine0() {
  IFS="\n"
  for m_md5_line in $(wget -O - "${m_base_url}/${m_base_name}.tar.md5.txt"); do
    m_md5_hash=$(echo -n "${m_md5_line}" | sed -rne 's/^([0-9a-f]{32} [ \*])[^\/]+\.[0-9]{2}$/\1/p') || return $?
    test -n "${m_md5_hash}" || return $?
    m_md5_name=$(echo -n "${m_md5_line}" | tail -c +35) || return $?
    test -n "${m_md5_name}" || return $?
    m_result=0
    routine1 "${m_base_url}" "${m_md5_line}" "${m_md5_name}" || m_result=$?
    rm -f "${m_md5_name}" || true
    return ${m_result}
  done
}

routine() {
  m_result=0
  m_temp_directory=$(mktemp --directory "download.XXXXXX") || return $?
  (cd "${m_temp_directory}" && routine0) || m_result=$?
  rm -rf "${m_temp_directory}" || true
  return ${m_result}
}

routine
