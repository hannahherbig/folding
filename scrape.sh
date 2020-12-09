#!/bin/bash -ex

paths=(
    donors
    teams
    donors-monthly
    teams-monthly
    donor/andrew12
    team/45032
)

for path in ${paths[@]}
do
    out=data/$path
    mkdir -p $(dirname $out)
    curl -s https://stats.foldingathome.org/api/$path -o $out.json
done
