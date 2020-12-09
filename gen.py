import subprocess
from datetime import datetime, timedelta
from glob import iglob
from itertools import chain
from pathlib import Path
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


class Item(BaseModel):
    last: datetime
    credit: int
    wus: int
    last_change: Optional[timedelta] = None
    credit_change: Optional[int] = None
    wus_change: Optional[int] = None
    ppd: Optional[int] = None


def write_table(repo, name):
    commits = git_commits_for(name)

    rows = {}
    for ref in commits:
        blob = repo.commit(ref).tree[name].data_stream.read()
        i = Item.parse_raw(blob)
        rows[i.last] = i

    table = []
    for a, b in pairwise(sorted(rows.values(), key=lambda i: i.last, reverse=True)):
        a.last_change = a.last - b.last
        a.credit_change = a.credit - b.credit
        a.wus_change = a.wus - b.wus
        a.ppd = int(a.credit_change / a.last_change.total_seconds() * 86400)
        table.append(a.dict())

    Path(name).with_suffix(".txt").write_text(tabulate(table, headers="keys") + "\n")


repo = git.Repo(".", odbt=git.db.GitCmdObjectDB)

for name in chain(iglob("data/donor/*.json"), iglob("data/team/*.json")):
    write_table(repo, name)
