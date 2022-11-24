import os

from collections import deque
from lark import Token
from lark.visitors import Visitor_Recursive
from commands import Call, Pipe, Sequence


class ASTConstructor(Visitor_Recursive):
    def __init__(self, in_stream, out_stream):
        self.in_stream = in_stream
        self.out_stream = out_stream

        self.tokens = deque()
        self.apps = deque()

        self.input_redirection = False
        self.output_redirection = ""

    def start(self, t):
        self.apps.popleft().eval(self.in_stream, self.out_stream)

    def seq(self, t):
        app1 = self.apps.popleft()
        app2 = self.apps.popleft()
        self.apps.append(Sequence(app1, app2))

    def pipe(self, t):
        app1 = self.apps.popleft()
        app2 = self.apps.popleft()
        self.apps.append(Pipe(app1, app2))

    def call(self, t):
        app = self.tokens.popleft()
        args = []

        while self.tokens:
            args.append(self.tokens.popleft())

        self.apps.append(Call(app, args))

    def r_dir(self, t):
        if self.output_redirection != "":
            return ValueError("Mutiple output redirection is not allowed")

        path = self.tokens.pop()

        with open(path, "w") as f:
            pass

        self.output_redirection = path

    def l_dir(self, t):
        if self.input_redirection:
            return ValueError("Mutiple input redirection is not allowed")

        path = self.tokens.pop()

        if not os.path.isfile(path):
            return ValueError("Wrong path or file does not exist input")

        with open(path, "r") as f:
            self.in_stream.append(f.read())

        self.input_redirection = True

    def argument(self, t):
        if isinstance(t.children[0], Token):
            self.tokens.append(str(t.children[0]))

    def quote(self, t):
        self.tokens.append(str(t.children[0]))

    def back_quoted(self, t):
        from shell import exec

        content = t.children[0]
        # parse the content again, execute it and return the result
        in_stream = deque()
        out_stream = deque()
        exec(content, in_stream, out_stream)
        self.tokens.append("".join(out_stream))
