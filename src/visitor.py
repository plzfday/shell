import os

from collections import deque
from glob import glob
from lark import Token
from lark.visitors import Visitor_Recursive
from commands import Call, Pipe, Sequence
from exceptions import NotSingleRedirectionError, InvalidPathError


class ASTConstructor(Visitor_Recursive):
    def __init__(self, in_stream, out_stream):
        self.in_stream = in_stream
        self.out_stream = out_stream

        self.tokens = deque()
        self.substitutions = deque()
        self.apps = deque()

        self.input_redirection = False
        self.output_redirection = ""

    def start(self, t):
        self.apps.popleft().eval(self.in_stream, self.out_stream)

    def seq(self, t):
        app2 = self.apps.pop()
        app1 = self.apps.pop()
        self.apps.append(Sequence(app1, app2))

    def pipe(self, t):
        app2 = self.apps.pop()
        app1 = self.apps.pop()
        self.apps.append(Pipe(app1, app2))

    def call(self, t):
        app = self.tokens.popleft()
        args = []

        while self.tokens:
            args.append(self.tokens.popleft())
        self.apps.append(Call(app, args, self.output_redirection))
        self.output_redirection = ""

    def r_dir(self, t):
        if self.output_redirection != "":
            raise NotSingleRedirectionError

        path = self.tokens.pop()
        self.output_redirection = path

    def l_dir(self, t):
        if self.input_redirection:
            raise NotSingleRedirectionError

        path = self.tokens.pop()

        if not os.path.isfile(path):
            raise InvalidPathError

        with open(path, "r") as f:
            self.in_stream.extend(f.readlines())

        self.input_redirection = True

    def argument(self, t):
        s = []
        for child in t.children:
            if isinstance(child, Token):
                globbing = sorted(glob(str(child)))
                if globbing:
                    s.extend(" ".join(globbing))
                else:
                    s.append(str(child))
            elif child.data == "double_quoted":
                s.append(self.tokens.pop())
            elif child.data == "back_quoted":
                s.append(self.substitutions.popleft())
        if len(s) != 0:
            self.tokens.extend("".join(s).split(' '))

    def single_quoted(self, t):
        self.tokens.append(t.children[0])

    def double_quoted(self, t):
        s = []
        for i in t.children:
            if isinstance(i, Token):
                s.append(str(i))
            else:
                s.append(self.substitutions.popleft())
        self.tokens.append("".join(s))

    def back_quoted(self, t):
        from shell import exec

        content = t.children[0]
        # parse the content again, execute it and return the result
        in_stream = deque()
        out_stream = deque()
        exec(content, in_stream, out_stream)
        res = [line.rstrip("\n") + " " for line in out_stream]
        self.substitutions.append("".join(res).rstrip("\n "))
