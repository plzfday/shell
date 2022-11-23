from lark.visitors import Visitor_Recursive
from commands import Call, Pipe, Sequence
import glob


class ASTConstructor(Visitor_Recursive):
    def __init__(self, in_stream, out_stream):
        self.in_stream = in_stream
        self.out_stream = out_stream

        self.tokens = []

    def seq(self, t):
        app1 = t.children[0]
        app2 = t.children[1]
        command = Sequence(app1, app2)
        command.eval(self.in_stream, self.out_stream)
        print("Sequence called", t.children)

    def pipe(self, t):
        app1 = t.children[0]
        app2 = t.children[1]
        command = Pipe(app1, app2)
        command.eval(self.in_stream, self.out_stream)
        print("Pipe called", t.children)

    def call(self, t):
        app = t.children[0]
        if app[0] == " ":
            app = t.children[1]

    def r_dir(self, t):
        print("Rdir called", t.children)

    def l_dir(self, t):
        print("Ldir called", t.children)

    def single_quoted(self, t):
        print("Single quoted called", t.children)

    def double_quoted(self, t):
        print(t.children[1])
        print("Double quoted called", t.children)

    def back_quoted(self, t):
        content = t.children[0]
        # parse the content again, execute it and return the result
        print("Back quoted called", content)
