from lark.visitors import Visitor_Recursive


class ASTConstructor(Visitor_Recursive):
    def __init__(self, in_stream, out_stream):
        self.in_stream = in_stream
        self.out_stream = out_stream

    def command(self, t):
        pass

    def seq(self, t):
        pass

    def call(self, t):
        pass

    def argument(self, t):
        pass

    def r_dir(self, t):
        pass

    def l_dir(self, t):
        pass

    def single_quoted(self, t):
        pass

    def double_quoted(self, t):
        pass

    def back_quoted(self, t):
        pass
