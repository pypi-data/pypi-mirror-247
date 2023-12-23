#  Copyright (c) Kuba Szczodrzyński 2022-8-24.

import sys
from subprocess import Popen
from time import sleep

import click

HAS_ERROR = False


def info(*msg):
    click.secho("[INFO] " + " ".join(map(str, msg)), fg="green")


def warn(*msg):
    click.secho("[WARN] " + " ".join(map(str, msg)), fg="yellow")


def error(*msg):
    global HAS_ERROR
    click.secho("[ERROR] " + " ".join(map(str, msg)), fg="red")
    HAS_ERROR = True


def error_exit():
    if HAS_ERROR:
        exit(1)


def error_clear():
    global HAS_ERROR
    HAS_ERROR = False


def command(*args):
    args = [str(arg) for arg in args]
    if sys.platform != "linux":
        print(*args)
        return
    count = 0
    while count < 10:
        p = Popen(args)
        p.wait()
        if p.returncode != 0:
            warn(
                f"Command '{' '.join(args)}' failed with return code {p.returncode}, retrying..."
            )
            sleep(2)
        else:
            return
        count += 1
    error(f"Command failed {count} times")
    error_clear()
