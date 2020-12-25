import hashlib
from os.path import join
from app.settings import DATA_DIR
import csv
from typing import Union, Tuple
from random import choice


def hash_string(data: str):
    return hashlib.sha256(str.encode(data)).hexdigest()


def make_clear_obfuscated_dict(path=None):
    if path is None:
        path = DATA_DIR
    with open(join(path, "list.csv"), encoding='utf-8') as csv_file:
        raw_list = list(csv.reader(csv_file, delimiter=","))
        return dict([(hash_string(t_id), '') for t_id, _, _ in raw_list])


def update_from_out_file(obfuscated_dict, path=None):
    if path is None:
        path = DATA_DIR
    file_path = join(path, "out.csv")

    open(file_path, 'a').close()
    with open(file_path, "r", encoding='utf-8') as csv_file:
        raw_obfuscated_list = list(csv.reader(csv_file, delimiter=","))
        obfuscated_dict.update(raw_obfuscated_list)


def write_to_out_file(obfuscated_dict, path=None):
    if path is None:
        path = DATA_DIR
    with open(join(path, "out.csv"), 'w', encoding='utf-8') as out:
        for obfuscated_id, data in obfuscated_dict.items():
            out.write(f"{obfuscated_id},{data}\n")


def make_obfuscation_map(path=None):
    if path is None:
        path = DATA_DIR
    obfuscation_map = None
    vk_map = None
    with open(join(path, "list.csv"), encoding='utf-8') as csv_file:
        obfuscation_map = dict([(hash_string(t_id), name) for t_id, name, vk in csv.reader(csv_file, delimiter=",")])
    with open(join(path, "list.csv"), encoding='utf-8') as csv_file:
        vk_map = dict([(name, vk) for t_id, name, vk in csv.reader(csv_file, delimiter=",")])
    return obfuscation_map, vk_map


def init(path=None):
    obfuscated_dict = make_clear_obfuscated_dict(path)
    update_from_out_file(obfuscated_dict, path)
    write_to_out_file(obfuscated_dict, path)

    return obfuscated_dict


OBFUSCATION_MAP, VK_MAP = make_obfuscation_map()
_obfuscated_dict = init()


def _choose_secret_name(hashed_id: str) -> str:
    free_unique_names = set(OBFUSCATION_MAP.values())
    free_unique_names -= set([OBFUSCATION_MAP[hashed_id]]) | set(_obfuscated_dict.values())
    return choice(list(free_unique_names))


def give_secret_name(telegram_id: str) -> Union[Tuple[bool, str], None]:
    hashed_id = hash_string(telegram_id)
    if hashed_id not in OBFUSCATION_MAP:
        return None

    if _obfuscated_dict[hashed_id]:
        return True, _obfuscated_dict[hashed_id]
    else:
        secret_name = _choose_secret_name(hashed_id)
        _obfuscated_dict[hashed_id] = secret_name
        write_to_out_file(_obfuscated_dict)
        return False, secret_name


if __name__ == '__main__':
    from pprint import pprint
    pprint(_obfuscated_dict)
    telegram_id = '4'
    print(give_secret_name(telegram_id))

