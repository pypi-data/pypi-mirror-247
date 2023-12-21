import json
import datetime
from typing import Any
from EasyToCacheLib.datetime_helper import cache_datetime, decrypt_datetime
from collections import OrderedDict
from EasyToCacheLib.etc_infrastructure import *


class Cache:
    def __init__(self, cache_path: str, load_from_json=True):
        self.__cache_path = get_relevant_path(cache_path)
        self.__cache = OrderedDict()
        if load_from_json:
            self.__cache = OrderedDict(self.__load_from_json())

        self.__write_on_disk = False
        self.__key_handler = lambda key: True
        self.__value_handler = lambda value: True

        self.__loading_from_json_handler = decrypt_datetime
        self.__writing_to_json_handler = cache_datetime

    def set_json_handlers(self, loading_from_json_handler=decrypt_datetime, writing_to_json_handler=cache_datetime):
        self.__loading_from_json_handler = loading_from_json_handler
        self.__writing_to_json_handler = writing_to_json_handler
        return self

    @property
    def length(self) -> int:
        return len(self.__cache)

    def add(self, key, value):
        """Add one value to cache by key"""
        if self.__key_handler(key) and self.__value_handler(value):
            if key in self.__cache.keys():
                self.__cache.pop(key)
            self.__cache[key] = (value, datetime.datetime.now())
        if self.__write_on_disk:
            self.write_to_json()
        return self

    def update(self, key, value):
        """Update value by key"""
        if key in self.__cache.keys():
            creation_time = self.__cache[key][1]
            self.__cache[key] = (value, creation_time)
        return self

    def remove(self, *keys):
        """Remove some values by keys"""
        for key in keys:
            if key in self.__cache.keys():
                self.__cache.pop(key)
        return self

    def get(self, key) -> Any:
        """Return value by key if it is in cache, else None"""
        return self.__cache[key][0]

    def get_creation_time(self, key) -> Any:
        """Return creation time by key if it is in cache, else None"""
        return self.__cache[key][1]

    def try_get(self, key) -> Any:
        """Return value if it is in cache, else None"""
        if key in self.__cache.keys():
            return self.__cache[key][0]
        return None

    def pop_items(self, index=-1) -> (Any, Any):
        last_key = list(self.__cache.keys())[index]
        value = self.__cache.pop(last_key)
        return last_key, value

    def get_dict(self) -> OrderedDict:
        return self.__cache

    def take(self, count: int):
        if len(self.__cache) <= count:
            return self

        new_cache = {}
        index = 0
        for key, value in self.__cache.items():
            if index == count:
                break
            new_cache[key] = value
            index += 1
        self.__cache = new_cache
        return self

    def skip(self, count: int):
        new_cache = {}
        if len(self.__cache) <= count:
            self.__cache = new_cache
            return self

        index = 0
        for key, value in self.__cache.items():
            index += 1
            if index <= count:
                continue
            new_cache[key] = value
        self.__cache = new_cache
        return self

    def clear(self):
        """Clear cache"""
        self.__cache.clear()
        return self

    def set_key_handler(self, key_handler):
        """Set key handle function"""
        self.__key_handler = key_handler
        new_cache = {}
        for key, value in self.__cache.items():
            if self.__key_handler(key):
                new_cache[key] = value
        self.__cache = new_cache
        return self

    def set_value_handler(self, value_handler):
        """Set value handle function"""
        self.__value_handler = value_handler
        new_cache = {}
        for key, value in self.__cache.items():
            if self.__value_handler(value[0]):
                new_cache[key] = value
        self.__cache = new_cache
        return self

    def sort_by_date(self, reverse=False):
        """Sort cache by it creation date, from recent to old"""
        self.__cache = dict(sorted(list(self.__cache.items()), key=lambda x: x[1], reverse=not reverse))
        return self

    def sort_by_value(self, reverse=False):
        """Sort cache by it values"""
        self.__cache = dict(sorted(list(self.__cache.items()), key=lambda x: x[0], reverse=reverse))
        return self

    def sort_by_key(self, reverse=False):
        """Sort cache by it keys"""
        self.__cache = dict(sorted(self.__cache.items(), reverse=reverse))
        return self

    def revere(self):
        self.__cache = OrderedDict(reversed(list(self.__cache.items())))
        return self

    def contain(self, key) -> bool:
        if key in self.__cache.keys():
            return True
        return False

    def set_writing_to_json_after_adding(self, writing: bool):
        self.__write_on_disk = writing
        return self

    def clear_json(self) -> None:
        with open(self.__cache_path, "w", encoding='utf-8'):
            pass

    def write_to_json(self) -> None:
        with open(self.__cache_path, "w", encoding='utf-8') as write_file:
            json.dump(self.__cache, write_file, ensure_ascii=False, default=self.__writing_to_json_handler)

    def __load_from_json(self) -> dict:
        try:
            with open(self.__cache_path, "r", encoding='utf-8') as read_file:
                file_data = read_file.read()
                if file_data.strip() != "":
                    return json.loads(file_data, object_hook=self.__loading_from_json_handler)
        except FileNotFoundError:
            self.clear_json()
        return {}


def main():
    pass


if __name__ == "__main__":
    main()
