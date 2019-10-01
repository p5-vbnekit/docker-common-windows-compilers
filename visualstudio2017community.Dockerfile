ARG base_image="chocolatey"
FROM ${base_image}
RUN choco install --confirm --ignoredetectedreboot dotnetfx
RUN choco install --confirm dotnetfx\nif "%ERRORLEVEL%" EQU "3010" exit 0
RUN choco install --confirm dotnetfx
RUN choco install --confirm visualstudio2017community
#RUN choco install --confirm visualstudio2017community --package-parameters "--allWorkloads --includeRecommended --includeOptional --passive --locale en-US"
