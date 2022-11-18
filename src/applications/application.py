import abc


class Application(metaclass=abc.ABCMeta):
    @staticmethod
    def by_name(name):
        if name == "pwd":
            from applications.pwd import Pwd

            return Pwd()
        elif name == "cd":
            from applications.cd import Cd

            return Cd()
        elif name == "cut":
            from applications.cut import Cut

            return Cut()
        elif name == "echo":
            from applications.echo import Echo

            return Echo()
        elif name == "ls":
            from applications.ls import Ls

            return Ls()
        elif name == "cat":
            from applications.cat import Cat

            return Cat()
        elif name == "head":
            from applications.head import Head

            return Head()
        elif name == "tail":
            from applications.tail import Tail

            return Tail()
        elif name == "grep":
            from applications.grep import Grep

            return Grep()
        elif name == "uniq":
            from applications.uniq import Uniq

            return Uniq()
        elif name == "find":
            from applications.find import Find

            return Find()
        else:
            raise ValueError(f"unsupported application {name}")

    @abc.abstractmethod
    def exec(self, args, out):
        raise NotImplementedError
