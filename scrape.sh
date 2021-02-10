#!/bin/bash -ex

paths=(
    donors
    teams
    donors-monthly
    teams-monthly
    donor/andrew12
    team/45032
    team/212997
    team/236565
)

for path in ${paths[@]}
do
    out=data/$path
    mkdir -p $(dirname $out)
    curl -s https://stats.foldingathome.org/api/$path | jq 'del(.total_users)' > $out.json
done
