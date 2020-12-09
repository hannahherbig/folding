import json
import subprocess

import git


def git_commits_for(path):
    return (
        subprocess.check_output(["git", "log", "--format=%H", path])
        .strip()
        .decode()
        .splitlines()
    )


repo = git.Repo(".", odbt=git.db.GitCmdObjectDB)
name = "data/team/45032.json"
commits = git_commits_for(name)

for ref in commits:
    blob = repo.commit(ref).tree[name].data_stream.read()
    donor = json.loads(blob)
    print(donor["last"], donor["credit"], donor["wus"])
