import contextlib
from abc import ABC, abstractmethod
from dataclasses import dataclass

from utils.errno import Error
from utils.server import Context
from utils.time import get_now_stamp_float


@dataclass
class FToken:
    client: str
    deadline: float
    token: str

    _sep = "+"

    @classmethod
    def parse(cls, s: str):
        s = s.split(cls._sep)
        if len(s) != 3:
            return None
        return cls(client=s[0], deadline=float(s[1]), token=s[2])

    def to_str(self):
        return f"{self.client}{self._sep}{self.deadline}{self._sep}{self.token}"

    def dead(self) -> bool:
        return get_now_stamp_float() > self.deadline

    def same(self, token: str) -> bool:
        return self.token == token


class Base(ABC):
    @abstractmethod
    @contextlib.contextmanager
    def ing(self, ctx: Context, target: str, client: str) -> Error:
        pass

    @abstractmethod
    def acquire(self, target: str, client: str, timeout: int) -> tuple[str, Error]:
        pass

    @abstractmethod
    def release(self, target: str, token: str) -> Error:
        pass
