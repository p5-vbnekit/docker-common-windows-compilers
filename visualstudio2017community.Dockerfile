ARG base_image="chocolatey"
FROM ${base_image}
#RUN choco install --confirm visualstudio2017community --package-parameters "--allWorkloads --includeRecommended --includeOptional --passive --locale en-US"
RUN choco install --confirm visualstudio2017community
