#!/bin/bash -ex

paths=(
    donors
    teams
    donor/andrew12
    team/45032
)

add_run() {
    git add -A
    pre-commit run
}

find . -name '*.json' -delete

for path in ${paths[@]}
do
    out=data/$path
    mkdir -p $(dirname $out)
    curl https://stats.foldingathome.org/api/$path > $out.json
done

npx prettier -w .
git add -A
git config --local user.name "github-actions[bot]"
git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"
git commit -m update || exit 0
git push
