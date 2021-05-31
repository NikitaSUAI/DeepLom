import os
import sys

from ipcqueue import posixmq


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise BaseException("Karamba!!!")

    mq = posixmq.Queue(sys.args[-1])
    while True:
        msg = mq.get()

