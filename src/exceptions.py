class InvalidFlag(Exception):
    def __init__(self):
        super().__init__("invalid flags")

class WrongNumberOfArguments(Exception):
    def __init__(self):
        super().__init__("wrong number of command line arguments")

class InvalidPath(Exception):
    def __init__(self):
        super().__init__("wrong path or file does not exist")

class InvalidRange(Exception):
    def __init__(self):
        super().__init__("invalid range")

class InvalidInput(Exception):
    def __init__(self):
        super().__init__("invalid input")

class PatternNotFound(Exception):
    def __init__(self):
        super().__init__("pattern cannot be found")

class UnknownApplciation(Exception):
    def __init__(self, name):
        super().__init__(f"Unknown application: {name}")

class NotSingleRedirection(Exception):
    def __init__(self):
        super().__init__("mutiple redirection is not allowed")


# ValueError(f"unexpected command line argument {sys.argv[1]}")