import subprocess
import os
from typing import List
from .comp import Writeup

def init() -> None:
    owd = os.getcwd()
    wd = 'site'
    if not os.path.exists(wd):
        subprocess.run(['git', 'clone', 'https://github.com/silasary/CardContest.git', wd], check=True)
    os.chdir(wd)
    subprocess.run(['git', 'pull'], check=True)
    os.chdir(owd)

def drafts() -> List[Writeup]:
    drafts = os.scandir(os.path.join('site', '_drafts'))
    return [Writeup(d.path) for d in drafts]

def commit(msg: str) -> None:
    owd = os.getcwd()
    wd = 'site'
    os.chdir(wd)
    subprocess.run(['git', 'add', '--all'], check=True)
    subprocess.run(['git', 'commit', '-m', msg], check=True)
    os.chdir(owd)
