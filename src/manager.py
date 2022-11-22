import os

from lark import Lark
from visitor import ASTConstructor


class ShellManager:
    def __init__(self, in_stream, out_stream):
        self.in_stream = in_stream
        self.out_stream = out_stream

        self.__GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), "grammars")
        self.__FILE_NAME = "shell.lark"
        grammar = open(self.__GRAMMAR_FILE, self.__FILE_NAME).read()
        self.__parser = Lark(grammar, start="command")

    def parse(self, cmdline):
        tree = self.__parser.parse(cmdline)
        visitor = ASTConstructor(self.in_stream, self.out_stream)
        visitor.visit(tree)
