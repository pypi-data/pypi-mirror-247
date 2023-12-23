#  Copyright (c) Kuba Szczodrzyński 2022-8-24.

import os
import signal
import sys
from pathlib import Path
from subprocess import PIPE, Popen
from threading import Thread
from time import time

import click
from click import Context

from .config import Config
from .manager import SnapManager
from .utils import error, info, warn

PROC_LIST: list = [None, None]
PROC_FLAG: list = [False]


def log_thread(*command: str):
    while not PROC_FLAG[0]:
        info("Executing:", *command)
        p = Popen(command, stdin=PIPE, stderr=PIPE)
        PROC_LIST[1] = p
        p.wait()


@click.group()
@click.argument("WORKDIR", type=click.Path(dir_okay=True, path_type=Path))
@click.pass_context
def cli(ctx: Context, workdir: Path):
    config = Config(workdir=workdir.absolute())
    manager = SnapManager(config)
    ctx.obj = (config, manager)
    paths = [
        config.data_rw_path,
        config.data_ro_path,
        config.mnt_path,
        config.root_path,
        config.snaps_path,
        config.work_path,
    ]
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


@cli.command(help="Configure (add snaps)")
@click.pass_context
def configure(ctx: Context):
    (config, manager) = ctx.obj
    config: Config
    manager: SnapManager

    config.validate(interactive=True)
    manager.fetch()
    config.validate()
    manager.refresh()
    manager.install()


@cli.command(help="Update snaps")
@click.option("-n", "--dry-run", help="Print what needs to be updated", is_flag=True)
@click.pass_context
def update(ctx: Context, dry_run: bool):
    (config, manager) = ctx.obj
    config: Config
    manager: SnapManager

    config.validate()
    manager.fetch()
    manager.refresh()
    manager.install(dry_run=dry_run)


@cli.command(help="Run a command inside chroot")
@click.argument("CMD", nargs=-1, type=str)
@click.option("-R", "--no-refresh", help="Do not refresh before running", is_flag=True)
@click.option("-I", "--no-install", help="Do not install before running", is_flag=True)
@click.option("-b", "--bind", help="Bind-mounts for chroot", type=str, multiple=True)
@click.option("-l", "--log", help="Watch (tail) specified log file", type=str)
@click.option("-L", "--clear-log", help="Remove log file before running", is_flag=True)
@click.option("-r", "--restart", help="Restart process N times if it dies", type=int)
@click.option("-t", "--trace", help="Run strace, wait for FIFO reader", is_flag=True)
@click.pass_context
def run(
    ctx: Context,
    no_refresh: bool,
    no_install: bool,
    bind: tuple[str],
    log: str,
    clear_log: bool,
    restart: int,
    trace: bool,
    cmd: tuple[str],
):
    (config, manager) = ctx.obj
    config: Config
    manager: SnapManager

    config.validate()
    manager.fetch()

    if not cmd:
        cmd = ["/bin/bash"]
    if not no_refresh:
        manager.refresh()
    if not no_install:
        manager.install()
    if not all(snap.is_installed for snap in config.snaps):
        error("Not all snaps are installed, can't continue")
        exit(1)
    manager.mount_snaps()
    manager.mount_root(*bind)

    trace = trace and sys.platform == "linux"

    if trace:
        strace_log = config.data_rw_path / "strace.log"
        strace_calls = ["open", "openat", "connect", "accept", "stat", "unlink"]
        strace_cmd = ["strace", "-e", f"trace={','.join(strace_calls)}"]
        try:
            os.mkfifo(strace_log)
        except FileExistsError:
            pass
    else:
        strace_log = ""  # make lint happy
        strace_cmd = []

    if log:
        log_path = config.root_path / log
        if clear_log and log_path.is_file():
            log_path.unlink(missing_ok=True)
        tail_cmd = ["tail", "-n", "30", "-F", log]
    else:
        tail_cmd = []

    args = ["chroot", str(config.root_path), *strace_cmd, *cmd]
    log_args = ["chroot", str(config.root_path), *tail_cmd]

    def sigterm_handler(*_args):
        info("Terminating gracefully")
        # signal termination
        PROC_FLAG[0] = True
        # stop the log reader
        if PROC_LIST[1]:
            PROC_LIST[1].kill()
        # stop the main process
        if PROC_LIST[0]:
            PROC_LIST[0].kill()
        else:
            warn("Termination with no process, aborting now")
            manager.unmount_root()
            manager.unmount_snaps()
            exit(1)

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)

    if trace:
        info("Waiting for FIFO reader")
        stdout = stderr = strace_log.open("w")
    else:
        stdout = sys.stdout
        stderr = sys.stderr

    death_last = time()
    death_count = 0

    if log:
        info("Starting log reader thread")
        thread = Thread(target=log_thread, args=(*log_args,))
        thread.start()
    else:
        thread = None

    while not PROC_FLAG[0]:
        info("Executing:", *args)
        p = Popen(args, stdin=sys.stdin, stdout=stdout, stderr=stderr)
        PROC_LIST[0] = p
        p.wait()
        if not PROC_FLAG[0]:
            if not restart:
                break
            if time() - death_last > 20:
                death_count = 0
            death_last = time()
            death_count += 1
            warn(f"Subprocess died {death_count} time(s), restarting")
            if death_count >= restart:
                error(f"Subprocess cannot start!")
                break

    # stop the main process
    if PROC_LIST[0]:
        PROC_LIST[0].kill()
    # stop the log reader
    if PROC_LIST[1]:
        PROC_LIST[1].kill()

    if thread:
        thread.join()
    manager.unmount_root(*bind)
    manager.unmount_snaps()


if __name__ == "__main__":
    cli()
