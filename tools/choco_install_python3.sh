#!/bin/sh -e

m_normal_path="$1"
export PS4="executing command: "; set -xo pipefail

test -n "${m_normal_path}"
mkdir -p "${m_normal_path}"
m_ugly_path=$(cd "${m_normal_path}" && cmd.exe /c 'echo %cd%' | tail -n 1)
test -n "${m_ugly_path}"
choco install "python3" --confirm --params "/InstallDir:\"${m_ugly_path}\""
