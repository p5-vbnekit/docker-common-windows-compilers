ARG base_image="chocolatey"
FROM ${base_image}
RUN choco install --confirm --ignoredetectedreboot dotnetfx
RUN choco install --confirm dotnetfx
RUN choco install --confirm visualstudio2019community
#RUN choco install --confirm visualstudio2019community --package-parameters "--allWorkloads --includeRecommended --includeOptional --passive --locale en-US"
