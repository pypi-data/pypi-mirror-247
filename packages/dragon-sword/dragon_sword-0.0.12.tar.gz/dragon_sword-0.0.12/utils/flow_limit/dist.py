import contextlib
import time
from threading import Thread, Event
from abc import abstractmethod

from utils.data import CacheKey, uniq_id
from utils.errno import Error, OK, FLOW_LIMIT_NO_TOKEN, FLOW_LIMIT_NO_ACQUIRED
from utils.time import get_now_stamp_float, get_stamp_after
from utils.server import Context
from utils.log import logger

from .base import Base, FToken


class DistBase(CacheKey, Base):
    @abstractmethod
    def _con_limit(self) -> int:
        """
        获取并发数限制
        :return:
        """
        pass

    @abstractmethod
    def _get_key_value(self, key: str) -> tuple[str, Error]:
        pass

    @abstractmethod
    def _acquire(self, key: str, f_token: FToken) -> Error:
        """
        落盘占用，将token写入redis/文件等
        :param key:
        :param f_token:
        :return:
        """
        pass

    @abstractmethod
    def _renew(self, key: str, f_token: FToken) -> Error:
        pass

    @abstractmethod
    def _release(self, key: str) -> Error:
        """
        落盘解除占用
        :param key:
        :return:
        """
        pass

    def _key_prefix(self) -> str:
        return ""

    def _load(self, key: str):
        s, err = self._get_key_value(key)
        if not err.ok:
            return None
        return FToken.parse(s)

    def _same_exist(self, exist: FToken, token: str) -> bool:
        """
        :param exist:
        :param token:
        :return: 已占用的是否与新的一致
        """
        return exist.same(token)

    def _can_acquired(self, key: str, token: str, locked=False) -> bool:
        """
        是否能重新占据key
        :param key:
        :param token:
        :param locked:
        :return: 是否已被占用
        """
        if locked:
            exist: FToken = self._get(key)
        else:
            exist: FToken = self.get(key)
        # 未被使用
        if not exist:
            return True
        return self._same_exist(exist, token) or exist.dead()

    @staticmethod
    def _format_target(target: str) -> str:
        return target.replace(":", "_").replace("\\", "_")

    def _start_renew(self, target: str, token: str, event: Event, timeout: int):
        while not event.wait(timeout=timeout / 3):
            err = self.renew(target, token, timeout)
            if not err.ok:
                # TODO: handle err
                logger.error(f"renew {target} {token} err={err}")

    def _stop_renew(self, thread: Thread, event) -> Error:
        if thread is None or not thread.is_alive():
            return OK
        event.set()
        thread.join()

    @contextlib.contextmanager
    def ing(self, ctx: Context, target: str, client: str) -> Error:
        target = self._format_target(target)
        token_timeout = 10
        err = FLOW_LIMIT_NO_TOKEN
        token = ""
        while not err.ok and not ctx.timeoutd():
            token, err = self.acquire(target, client, token_timeout)
            if not err.ok:
                logger.error(f"!!!retry {target}")
                time.sleep(3)

        if not err.ok or not token:
            yield err
            return err

        event = Event()
        thread = Thread(target=self._start_renew, args=(target, token, event, token_timeout))
        thread.demon = True
        thread.start()
        yield OK
        self._stop_renew(thread, event)
        self.release(target, token)

    def acquire(self, target: str, client: str, timeout: int) -> tuple[str, Error]:
        """
        第一次请求
        :param target:
        :param timeout:
        :param client: 仅作记录
        :return:
        """
        target = self._format_target(target)
        token = uniq_id()
        for i in range(self._con_limit()):
            key = f"{self._key_prefix()}={target}={i}"
            if not self._can_acquired(key, token):
                continue

            with self._get_lock(key):
                if not self._can_acquired(key, token, locked=True):
                    continue

                err = self._acquire(key, FToken(
                    client=client,
                    deadline=get_stamp_after(get_now_stamp_float(), second=timeout),
                    token=token
                ))
                if err.ok:
                    self.update(key)
                    return token, OK
        return "", FLOW_LIMIT_NO_TOKEN

    def _can_renew(self, key: str, token: str, locked=False) -> tuple[FToken, bool]:
        """
        能否能续期token
        :param key:
        :param token:
        :param locked:
        :return: 是否能继续循环，能否能续期token
        """
        if locked:
            exist: FToken = self._get(key)
        else:
            exist: FToken = self.get(key)

        if not exist:
            return exist, False
        # 不用管是否过期，只要是同一个token，还没被覆盖
        return exist, self._same_exist(exist, token)

    def renew(self, target: str, token: str, timeout: int) -> Error:
        target = self._format_target(target)
        for i in range(self._con_limit()):
            key = f"{self._key_prefix()}={target}={i}"
            exist, can_renew = self._can_renew(key, token)
            if not can_renew:
                continue

            with self._get_lock(key):
                exist, can_renew = self._can_renew(key, token, locked=True)
                if not can_renew:
                    continue
                err = self._renew(key, FToken(
                    client=exist.client,
                    deadline=get_stamp_after(get_now_stamp_float(), second=timeout),
                    token=token
                ))
                self.update(key)
                return err
        return FLOW_LIMIT_NO_ACQUIRED

    def release(self, target: str, token: str) -> Error:
        target = self._format_target(target)
        for i in range(self._con_limit()):
            key = f"{self._key_prefix()}={target}={i}"
            exist = self.get(key)
            if not exist:
                continue
            if self._same_exist(exist, token):
                err = self._release(key)
                self.update(key)
                return err
        return OK
