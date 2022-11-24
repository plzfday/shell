from lark.visitors import Visitor_Recursive
from commands import Call, Pipe, Sequence
import os


class ASTConstructor(Visitor_Recursive):
    def __init__(self, in_stream, out_stream):
        self.in_stream = in_stream
        self.out_stream = out_stream

        self.tokens = []

        self.input_redirection = False
        self.output_redirection = ''

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
        # change the method to catch the app name
        app = t.children[0]
        contents = t.children[1:]
        print(app, contents)

        if app[0] == " ":
            app = t.children[1]
            contents = t.children[2:]

        # arguments are not guaranteed to be strings
        args = []
        # for arg in contents:
        #     print(args)
        #     if arg[0] != " ":
        #         args.append(arg)

        obj = Call(app, args)
        obj.eval(self.in_stream, self.out_stream)

    def r_dir(self, t):
        if self.output_redirection != '':
            return ValueError("Mutiple output redirection is not allowed")

        with open(t.children[1], 'w') as f:
            pass
        self.output_redirection = t.children[1]
        
        print("Rdir called", t.children)

    def l_dir(self, t):
        if self.input_redirection:
            return ValueError("Mutiple input redirection is not allowed")

        if not os.path.isfile(t.children[1]):
            return ValueError("Wrong path or file does not exist input")

        with open(t.children[1], 'r') as f:
            self.in_stream.append(f.read())
        self.input_redirection = True

        print("Ldir called", t.children)

    def single_quoted(self, t):
        self.tokens.append(t.children[0])

    def double_quoted(self, t):
        self.tokens.append(t.children[0])

    def back_quoted(self, t):
        content = t.children[0]
        # parse the content again, execute it and return the result
        print("Back quoted called", content)
