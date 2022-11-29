import re
import sys
from app import APP


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
    import platform
    if platform.system() == 'Windows':
        return getkey_windows
    else:
        return getkey_unix


def input(prompt: str):
    getkey = getkey_factory()

    app_list = tuple(APP.keys())
    s = ""

    print(prompt, end="", flush=True)
    while True:
        c = getkey()
        # control-c or control-d
        if c in ["\x03", "\x04"]:
            return None

        if c == "\r":
            print(flush=True)
            return s

        if c == "\x7f":
            s = s[:-1]
        else:
            s += c

        cmdline = []
        sep = 0
        for m in re.finditer("([^;|]+|\"[^\"]*\"|'[^']*')", s):
            cur = m.group(0).split()

            if not cur:
                if m.group(0).startswith(" "):
                    cmdline.append(m.group(0))
                continue

            cmd = cur[0].strip()
            line = m.group(0)
            color = 32 if cmd in app_list else 31
            cmdline.append(line.replace(cmd, f"\033[{color}m{cmd}\033[0m", 1))
            if len(s) > sep + len(line):
                cmdline.append(s[sep+len(line)])
                sep += len(line) + 1

        print(f"\033[2K\033[1G{prompt}{''.join(cmdline)}", end="", flush=True)
