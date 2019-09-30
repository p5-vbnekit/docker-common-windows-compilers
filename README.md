# docker-common-windows-compilers
Windows docker images with common compilers.<br/>
Based on ["mcr.microsoft.com/windows/servercore:1803" image](https://hub.docker.com/_/microsoft-windows-servercore).<br/>
Auomated builds and releases powered by [travis-ci](https://travis-ci.org/p5-vbnekit/docker-common-windows-compilers).
## Releases
### Links:
- [Latest release](../../releases/latest)
- [Releases history](../../releases)
Since [maximum release asset file size is limited by github](https://help.github.com/en/articles/about-releases#limitations-on-binary-files), I have to split them into parts.<br/>
This parts named as `${IMAGE}.tar.xz.${NN}`.<br/>
Each asset image is accompanied by md5 list text file: `${IMAGE}.tar.xz.md5.txt`.<br/>
Just download all parts of the current image and call something like: `cat ${IMAGE}.tar.xz.* | xz --decompress --stdout | docker load`.<br/>
Also you can use [this script (tools/download_released_image.py)](tools/download_released_image.py): `python3 tools/dowload_released_image.py "name: ${IMAGE}.tar.xz" | xz --decompress --stdout | docker load`
## Images
### chocolatey
Based on ["mcr.microsoft.com/windows/servercore:1803" image](https://hub.docker.com/_/microsoft-windows-servercore).</br>
Added ["chocolatey" package manager](https://chocolatey.org).
### msys2
Based on ["chocolatey"](#chocolatey) image.<br/>
Added ["msys2" chocolatey package](https://chocolatey.org/packages/msys2) with:
- mingw32/mingw-w64-i686-gcc
- mingw64/mingw-w64-x86_64-gcc
### visualstudio2017community
Based on ["chocolatey"](#chocolatey) image with ["Visual Studio 2017 Community" chocolatey package](https://chocolatey.org/packages/VisualStudio2017Community).
### visualstudio2019community
Based on ["chocolatey"](#chocolatey) image with ["Visual Studio 2019 Community" chocolatey package](https://chocolatey.org/packages/VisualStudio2019Community).
