import sys


def stdinput():
    sin = sys.stdin
    sout = sys.stdout
    while True:
        try:
            s = sin.readline()
            sout.write(s)
        except KeyboardInterrupt:
            break
