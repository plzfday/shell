class InvalidFlagError(Exception):
    def __init__(self):
        super().__init__("invalid flags")


class WrongNumberOfArgumentsError(Exception):
    def __init__(self):
        super().__init__("wrong number of command line arguments")


class InvalidPathError(Exception):
    def __init__(self):
        super().__init__("wrong path or file does not exist")


class InvalidRangeError(Exception):
    def __init__(self):
        super().__init__("invalid range")


class InvalidInputError(Exception):
    def __init__(self):
        super().__init__("invalid input")


class PatternNotFoundError(Exception):
    def __init__(self):
        super().__init__("pattern cannot be found")


class UnknownApplicationError(Exception):
    def __init__(self, name):
        super().__init__(f"Unknown application: {name}")


class NotSingleRedirectionError(Exception):
    def __init__(self):
        super().__init__("mutiple redirection is not allowed")
