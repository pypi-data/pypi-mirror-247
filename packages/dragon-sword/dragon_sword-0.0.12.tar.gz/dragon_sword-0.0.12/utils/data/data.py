import hashlib
import json
import re
import sys
import uuid
import zlib
from ast import literal_eval
from collections import OrderedDict
from dataclasses import asdict


def format_file_name(name: str, version: int = sys.maxsize) -> str:
    """
    规范化文件名中，一些会导致显示异常的字符
    :param name:
    :param version: 1原样 2替换|/\\
    :return:
    """
    if version == 1:
        return name

    name = name.replace("|", "_").replace("/", "").replace("\\", "")
    if version <= 2:
        return name

    # 版本3除了下面替换，还有最后的去空格和_
    if version >= 3:
        name = name.replace("\n", " ").replace("\r\n", " ")
        # -不能换成_
        name = name.replace("……", "_").replace('"', "_").replace("'", "_") \
            .replace("！", " ").replace("!", " ") \
            .replace(",", " ").replace(".", " ") \
            .replace("，", " ").replace("。", " ") \
            .replace("[", " ").replace("]", " ") \
            .replace("【", " ").replace("】", " ")

    if version >= 4:
        name = name.replace("(", " ").replace(")", " ") \
            .replace("~", " ") \
            .replace("&", " ") \
            .replace("$", " ") \
            .replace("=", " ")

    name = name.strip()
    name = ' '.join(name.split())
    name = name.replace(" ", "_")
    return name


def md5(text):
    encode_pwd = text.encode()
    md5_pwd = hashlib.md5(encode_pwd)
    return md5_pwd.hexdigest()


def str_to_int(s: str):
    m = md5(s)
    return int(m, 16)


def is_num(s) -> bool:
    return isinstance(s, int) or isinstance(s, float) or s.replace('.', '', 1).isdigit()


def uniq_id() -> str:
    return uuid.uuid1().hex


def decode_gzip(b: bytes) -> bytes:
    try:
        return zlib.decompress(b, 16 + zlib.MAX_WBITS)
    except zlib.error:
        return b


def decode_bytes(b: bytes) -> tuple[str, bool]:
    try:
        return b.decode("utf-8"), True
    except UnicodeDecodeError:
        return "", False


_IntRegex = re.compile(r'\d+')


def get_ints_in_str(s: str) -> list[int]:
    ss = _IntRegex.search(s)
    result = []
    for s in ss:
        if is_num(s):
            result.append(int(s))
    return result


class LowStr(str):
    def __new__(cls, s: str):
        return str.__new__(cls, s.lower())


def get_first_by_order(data, order: tuple):
    for o in order:
        if o in data:
            return o
    return None


def merge_dict(a: dict, b: dict, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dict(a[key], b[key], path + [str(key)])
            elif a[key] != b[key]:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def trans_str(s: str):
    try:
        return literal_eval(s)
    except Exception:
        return s


def remove_list_duplicate(data: list):
    return list(OrderedDict.fromkeys(data))


def remove_list_dup_save_first(data: list):
    exist = set()
    result = [exist.add(item) or item for item in data if item not in exist]
    return result


class Data:
    def dict(self):
        return asdict(self)

    def __str__(self):
        return json.dumps(self.dict(), ensure_ascii=False, sort_keys=True)

    @classmethod
    def parse(cls, s: str):
        return cls(**json.loads(s))

    @classmethod
    def parse_dict(cls, d: dict):
        if not isinstance(d, dict):
            return d
        return cls(**d)
