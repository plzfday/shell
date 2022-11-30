import re
import sys

from app import APP
from history_manager import HistoryManager


def getkey_windows():
    import msvcrt
    return msvcrt.getch()


def getkey_unix():
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def getkey_factory():
    """ Windows and Unix systems have different ways to get keyboard input

    Thus, we need a factory method to return the correct function for OS.
    """
    import platform
    if platform.system() == "Windows":
        return getkey_windows
    else:
        return getkey_unix


def input(prompt: str):
    """ Catches the keyboard input and prints the line

    This function adapts MVC pattern. Because the string printed out for user
    is coloured which means it includes substrings like '[033', the actual
    string and the viewed string are treated differently.
    """
    getkey = getkey_factory()
    history = HistoryManager()

    app_list = tuple(APP.keys())
    s = ""
    prev_s = ""

    print(prompt, end="", flush=True)
    while True:
        c = getkey()
        # control-c or control-d
        if c in ["\x03", "\x04"]:
            return None
        # enter
        if c == "\r":
            print(flush=True)
            return s
        # backspace
        if c == "\x7f":
            s = s[:-1]
            print("\b \b", end="", flush=True)
        # arrow up or arrow down
        # Since it takes 3 keys in a row, getkey() is called for 3 times
        elif c == "\x1b":
            c = getkey()
            if c == "\x5b":
                c = getkey()
                if c == "\x41":
                    s = history.arrow_up()
                elif c == "\x42":
                    s = history.arrow_down()
        # backspace
        elif c > "\x1f":
            s += c

        # View part
        cmdline = []
        sep = 0
        # This regex separates CMD into SUBCMD by ';' and '|'
        for m in re.finditer("([^;|]+|\"[^\"]*\"|'[^']*')", s):
            # split() is used to take the first word of the SUBCMD
            cur = m.group(0).split()
            # In the case of SUBCMD being full of spaces or empty
            # `cur` is an empty list
            if not cur:
                # Although skipping, spaces should be printed out for the user
                # to see the current position of the cursor
                if m.group(0).startswith(" "):
                    cmdline.append(m.group(0))
                continue

            cmd = cur[0].strip()
            line = m.group(0)
            # 32 and 31 are the colour codes for green and red, respectively
            color = 32 if cmd in app_list else 31
            cmdline.append(line.replace(cmd, f"\033[{color}m{cmd}\033[0m", 1))
            # Print out ';' or '|' if there is any
            if len(s) > sep + len(line):
                cmdline.append(s[sep+len(line)])
                sep += len(line) + 1
        # Clear the current line and print out the prompt
        # followed by thecurrent command line
        print("\b \b" * (len(prev_s) + len(prompt)), end="", flush=True)
        print(f"\r{prompt}{''.join(cmdline)}", end="", flush=True)
        prev_s = s
