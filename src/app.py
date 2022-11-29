from applications.pwd import Pwd
from applications.sort import Sort
from applications.uniq import Uniq
from applications.find import Find
from applications.cut import Cut
from applications.grep import Grep
from applications.tail import Tail
from applications.head import Head
from applications.echo import Echo
from applications.cat import Cat
from applications.ls import Ls
from applications.cd import Cd
from applications.history import History

APP = {
    "pwd": Pwd,
    "cd": Cd,
    "ls": Ls,
    "cat": Cat,
    "echo": Echo,
    "head": Head,
    "tail": Tail,
    "grep": Grep,
    "cut": Cut,
    "find": Find,
    "uniq": Uniq,
    "sort": Sort,
    "history": History,
}


def app_by_name(name):
    if name not in APP:
        raise ValueError(f"Unknown application: {name}")

    return APP[name]()
