import os

from lark import Lark
from visitor import ASTConstructor


class ShellManager:
    def __init__(self, in_stream, out_stream):
        self.in_stream = in_stream
        self.out_stream = out_stream

        FILE_PATH = "grammars/shell.lark"
        GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), FILE_PATH)
        grammar = open(GRAMMAR_FILE).read()
        self.__parser = Lark(grammar, start="start")

    def parse(self, cmdline):
        tree = self.__parser.parse(cmdline)
        # print(tree.pretty())
        visitor = ASTConstructor(self.in_stream, self.out_stream)
        visitor.visit(tree)
