from utils.errno import Error
from utils.file import load_f, dump_f, get_file_path
from .base import FToken
from .dist import DistBase
from utils.server_config import CommonConf


class FLockBase(DistBase):
    """
    文件异步锁，即限流为1
    """

    def __init__(self):
        super().__init__()

    def _get_key_value(self, key: str) -> tuple[str, Error]:
        return load_f(self._path(key))

    def _acquire(self, key: str, f_token: FToken) -> Error:
        return dump_f(self._path(key), f_token.to_str())

    def _renew(self, key: str, f_token: FToken) -> Error:
        return self._acquire(key, f_token)

    def _release(self, key: str) -> Error:
        return dump_f(self._path(key), "")

    def _con_limit(self) -> int:
        return 1

    def _path(self, key):
        return get_file_path(CommonConf.flow_limit_path, key)
