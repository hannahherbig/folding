import subprocess
from datetime import datetime
from typing import Optional

import git
from more_itertools import pairwise
from pydantic import BaseModel
from tabulate import tabulate


def git_commits_for(path):
    return (
        subprocess.check_output(["git", "log", "--format=%H", path])
        .strip()
        .decode()
        .splitlines()
    )


repo = git.Repo(".", odbt=git.db.GitCmdObjectDB)
name = "data/donor/andrew12.json"
commits = git_commits_for(name)


class Item(BaseModel):
    last: datetime
    credit: int
    wus: int
    credit_change: Optional[int] = None
    wus_change: Optional[int] = None


rows = {}
for ref in commits:
    blob = repo.commit(ref).tree[name].data_stream.read()
    i = Item.parse_raw(blob)
    rows[i.last] = i

table = []
for a, b in pairwise(sorted(rows.values(), key=lambda i: i.last, reverse=True)):
    a.credit_change = a.credit - b.credit
    a.wus_change = a.wus - b.wus
    table.append(a.dict())

print(tabulate(table, headers="keys"))
