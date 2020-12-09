#!/usr/bin/env bash

paths=(
    donors
    teams
    donor/andrew12
    team/45032
)

rm -rf data

for path in ${paths[@]}
do
    out=data/$path
    mkdir -p $(dirname $out)
    curl https://stats.foldingathome.org/api/$path > $out.json
done

npx prettier -w .
