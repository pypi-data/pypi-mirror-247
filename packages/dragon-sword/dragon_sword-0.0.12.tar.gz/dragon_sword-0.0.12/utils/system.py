import os
import platform
import random
import socket
import subprocess
import threading
import time
from importlib import import_module
from utils.log import logger

# 秒数
DEFAULT_TIMEOUT = 30 * 60


def is_win() -> bool:
    """
    是否运行在windows下
    :return:
    """
    return platform.system().lower() == 'windows'


def is_linux() -> bool:
    """
    是否运行在linux下
    :return:
    """
    return platform.system().lower() == 'linux'


def fix_win_focus():
    """
    防止鼠标误触导致阻塞，但也会导致不响应ctrl+c
    :return:
    """
    print(f"patch windows console")
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)


def cur_pid() -> int:
    return os.getpid()


def cur_tid() -> int:
    return threading.currentThread().ident


def get_host_ip() -> str:
    """
    查询本机ip地址
    :return: ip
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def import_by_name(name: str):
    return import_module(name)


def run_cmd(cmd: list[str], env=None, timeout=DEFAULT_TIMEOUT) -> tuple[str, bool]:
    try:
        out = subprocess.check_output(
            cmd, timeout=timeout, env=env,
            # pass arguments as a list of strings
            # shell=True,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        )
        out = out.replace("\r\n", "\n")
        logger.debug(f"{cmd} output={out}")
        return out, True
    except subprocess.CalledProcessError as e:
        out = e.output
        logger.error(f"{cmd} output={out}")
        return out, False
    except (FileNotFoundError, PermissionError) as e:
        out = f"{e}"
        logger.error(f"{cmd} output={out}")
        return out, False


def sleep(sec: int, at_least: int = None):
    if not at_least:
        at_least = max(sec - 2 * sec // 3, 1)
    sec = random.randint(at_least, sec)
    # logger.info(f"sleep {interval} {sec}")
    time.sleep(sec)


class StoppableThread(threading.Thread):
    """
    Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition.
    """

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
