ARG base_image="chocolatey"
FROM ${base_image}

RUN choco install --confirm msys2
RUN \tools\msys64\usr\bin\pacman.exe --noconfirm -Suy
# RUN \tools\msys64\usr\bin\pacman.exe --noconfirm -Suy mingw32/mingw-w64-i686-gcc mingw64/mingw-w64-x86_64-gcc
RUN \tools\msys64\usr\bin\pacman.exe --noconfirm -Scc
