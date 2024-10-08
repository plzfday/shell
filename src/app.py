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
from applications.wc import Wc

from exceptions import UnknownApplicationError

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
    "wc": Wc,
}


def app_by_name(name):
    """ Returns the application class by name (factory method) """
    if name not in APP:
        raise UnknownApplicationError(name)

    return APP[name]()
