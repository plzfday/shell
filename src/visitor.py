from lark.visitors import Visitor_Recursive


class ASTConstructor(Visitor_Recursive):
    def __init__(self, in_stream, out_stream):
        self.in_stream = in_stream
        self.out_stream = out_stream

    def command(self, t):
        print("Command called", t.children)

    def seq(self, t):
        print("Sequence called", t.children)

    def call(self, t):
        print("Call called", t.children)

    def argument(self, t):
        print("Argument called", t.children)

    def r_dir(self, t):
        print("Rdir called", t.children)

    def l_dir(self, t):
        print("Ldir called", t.children)

    def single_quoted(self, t):
        print("Single quoted called", t.children)

    def double_quoted(self, t):
        print("Double quoted called", t.children)

    def back_quoted(self, t):
        print("Back quoted called", t.children)
