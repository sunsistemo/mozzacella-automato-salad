import sys
from random import randrange


def python_random():
    write = sys.stdout.buffer.write
    while True:
        bs = bytearray([randrange(256) for _ in range(8192)])
        try:
            write(bs)
        except BrokenPipeError:
            sys.exit(1)


if __name__ == "__main__":
    python_random()
