!/bin/sh -e

m_path="$1"
test -n "${m_path}"

mkdir -p "${m_path}"
cd "${m_path}"
cmd.exe /c 'echo "%cd%"' | tail -n 1
