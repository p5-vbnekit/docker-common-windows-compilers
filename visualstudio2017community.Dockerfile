ARG base_image="chocolatey"
FROM ${base_image}
RUN echo if ^"^%ERRORLEVEL^%^" EQU "3010" exit 0 > \skip-reboot.bat
RUN choco install --confirm --ignoredetectedreboot dotnetfx || \skip-reboot.bat
RUN choco install --confirm dotnetfx || \skip-reboot.bat
RUN choco install --confirm visualstudio2017community || \skip-reboot.bat
RUN del \skip-reboot.bat
#RUN choco install --confirm visualstudio2017community --package-parameters "--allWorkloads --includeRecommended --includeOptional --passive --locale en-US"
