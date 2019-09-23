# docker-common-windows-compilers
Windows docker images with common compilers.
Based on ["mcr.microsoft.com/windows/nanoserver:1803" image](https://hub.docker.com/_/microsoft-windows-nanoserver).

## Download
[Releases](../../releases)

## Images

### chocolatey
Based on ["mcr.microsoft.com/windows/nanoserver:1803" image](https://hub.docker.com/_/microsoft-windows-nanoserver) with:
- [Microsoft PowerShell](https://github.com/PowerShell/PowerShell-Docker/blob/master/release/stable/nanoserver/docker/Dockerfile)
- ["chocolatey" package manager](https://chocolatey.org)

### msys2
Based on "chocolatey" image
Added ["msys2" chocolatey package](https://chocolatey.org/packages/msys2) with:
- mingw32/mingw-w64-i686-gcc
- mingw64/mingw-w64-x86_64-gcc

### visualstudio2017community
Based on "chocolatey" image with ["Visual Studio 2017 Community" chocolatey package](https://chocolatey.org/packages/VisualStudio2017Community).

### visualstudio2019community
Based on "chocolatey" image with ["Visual Studio 2019 Community" chocolatey package](https://chocolatey.org/packages/VisualStudio2019Community).
