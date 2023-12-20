from contextlib import contextmanager

from utils.errno import Error, OK, FLOW_LIMIT
from utils.server import Context, SemM
from utils.system import sleep

from .base import Base


class MemFlowLimit(Base):
    def __init__(self, limits: dict[str, int], prefix: str = None):
        self._names = []
        for name, limit in limits.items():
            if prefix:
                name = f"{prefix}_{name}"
            SemM.register(name, limit)
            self._names.append(name)

    @contextmanager
    def ing(self, ctx: Context, target: str, client: str):
        if SemM.lock(target):
            yield OK
            SemM.unlock(target)
        else:
            yield FLOW_LIMIT

    def try_ing(self, ctx: Context, client: str):
        for name in self._names:
            with self.ing(ctx, target=name, client=client) as err:
                if not err.ok:
                    sleep(3)
                else:
                    prefix, group = name.split("_")
                    yield prefix, group

    def acquire(self, target: str, client: str, timeout: int) -> tuple[str, Error]:
        pass

    def release(self, target: str, token: str) -> Error:
        pass
