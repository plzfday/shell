import os
from applications.application import Application


class Pwd(Application):
    def exec(self, args, out):
        out.append(os.getcwd())
