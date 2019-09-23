ARG base_image="mcr.microsoft.com/windows/servercore:1803"
FROM ${base_image}
RUN powershell iex(iwr -useb https://chocolatey.org/install.ps1)
