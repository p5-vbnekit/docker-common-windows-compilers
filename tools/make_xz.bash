#/bin/bash -e

m_base_name="$1"

export PS4="executing command: "; set -xo pipefail

test -n "${m_base_name}"
test "x${m_base_name}" = "x$(basename ""${m_base_name}"")"

test -n "${TRAVIS_TAG}"
test -n "$(echo ""${TRAVIS_TAG}"" | sed -rne '/^[^\"]+$/p')"

test -d "${m_tools_directory_path}"
m_download_released_image_py_path="${m_tools_directory_path}/download_released_image.py"
test -f "${m_download_released_image_py_path}"

test -f "${m_python3_executable_path}"
test -x "${m_python3_executable_path}"

mkdir -p "/tmp/build/output"
m_temporary_tar_path="/tmp/build/output/${m_base_name}"

"${m_python3_executable_path}" "${m_download_released_image_py_path}" "name: \"${m_base_name}\"" "release: { draft: \"${TRAVIS_TAG}\"}" "token: {env: \"DOWNLOAD_TOKEN\"}" "output: \"${m_temporary_tar_path}\""
(xz -9 --to-stdout --threads=0 "${m_temporary_tar_path}"; rm -f "${m_temporary_tar_path}") | split --numeric-suffixes --bytes=2GB - "/tmp/build/assets/${m_base_name}.xz."
(cd "/tmp/build/assets" && md5sum "${m_base_name}".xz.* > "${m_base_name}.xz.md5.txt")
