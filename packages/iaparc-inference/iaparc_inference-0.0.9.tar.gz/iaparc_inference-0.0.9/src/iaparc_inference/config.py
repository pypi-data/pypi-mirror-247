"""Config reader class"""
import logging.config
import os
import json
from json.decoder import JSONDecodeError
from yaml import Loader, dump, load


LOGGER = logging.getLogger("Config")

class Config(dict):
    """
    Config reader class
    """
    def __init__(self, data=None):
        super(Config, self).__init__()
        if data:
            if isinstance(data, dict):
                self.__update(data, {})
            elif isinstance(data, str):
                filename = os.path.basename(data)
                ext = os.path.splitext(filename)[1]
                self.__path = data
                self.__ext = ext
                if ext == "json":
                    self.__update(self.load_json(data), {})
                elif ext == "yaml" or ext == "yml":
                    self.__update(self.load_yaml(data), {})
                else:
                    try:
                        self.__update(self.load_json(data), {})
                    except (JSONDecodeError,TypeError):
                        self.__update(self.load_yaml(data), {})
            else:
                raise ValueError("Unknown data format")

    @staticmethod
    def dump_yaml(data, file_name):
        '''Dump data to yaml file'''
        to_dump = data.copy()
        del to_dump['_Config__path']
        del to_dump['_Config__ext']
        with open(f"{file_name}", "w", encoding="utf-8") as f:
            dump(to_dump, f)

    @staticmethod
    def dump_json(data, file_name):
        '''Dump data to json file'''
        to_dump = data.copy()
        del to_dump['_Config__path']
        del to_dump['_Config__ext']
        with open(f"{file_name}", "w", encoding="utf-8") as f:
            f.writelines(json.dumps(to_dump, indent=4))

    def save(self):
        '''Save config to file'''
        try:
            if self.__ext.lower() == ".json":
                self.save_to_json(self.__path)
            elif self.__ext.lower() == ".yaml" or self.__ext.lower() == ".yml":
                self.save_to_yaml(self.__path)
            else:
                LOGGER.error("Cannot save file, unknown extenstion %s", self.__ext)
        except Exception:
            LOGGER.error("Cannot save config", exc_info=True)

    def save_to_json(self, filename):
        '''Save config to json file'''
        self.dump_json(self, filename)

    def save_to_yaml(self, filename):
        '''Save config to yaml file'''
        self.dump_yaml(self, filename)

    @staticmethod
    def load_json(config):
        '''Load json file'''
        with open(config, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    @staticmethod
    def load_yaml(config):
        '''Load yaml file'''
        with open(config, "r", encoding="utf-8") as f:
            data = load(f, Loader=Loader)
        return data

    def new(self, data):
        '''Create new config from data'''
        self.__update(data, {})

    def load(self, data, did):
        """load methode"""
        self.__update(data, did)

    def __update(self, data, did):
        dataid = id(data)
        did[dataid] = self
        for k in data:
            dkid = id(data[k])
            if dkid in did.keys():
                self[k] = did[dkid]
            elif isinstance(data[k], Config):
                self[k] = data[k]
            elif isinstance(data[k], dict):
                obj = Config()
                obj.load(data[k], did)
                self[k] = obj
                obj = None
            elif isinstance(data[k], list) or isinstance(data[k], tuple):
                self[k] = self._add_list(data[k], did)
            else:
                self[k] = data[k]

    def _add_list(self, data, did):
        lst = []
        for l in data:
            if isinstance(l, dict):
                obj = Config()
                obj.load(l, did)
                lst.append(obj)
                obj = None
            elif isinstance(l, list) or isinstance(l, tuple):
                lst.append(self._add_list(l, did))
            else:
                lst.append(l)
        if isinstance(data, tuple):
            lst = tuple(lst)
        return lst

    def __getattr__(self, key):
        return self.get(key, None)

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            self[key] = Config(value)
        else:
            self[key] = value

    def has_key(self, k):
        """ returns True if key is present in the config"""
        if k in self.keys():
            return True
        else:
            return False

    def update(self, *args):
        for obj in args:
            for k in obj:
                if isinstance(obj[k], dict):
                    self[k] = Config(obj[k])
                else:
                    self[k] = obj[k]
        return self

    def merge(self, *args):
        """ merges the config with one or more configs"""
        for obj in args:
            for k in obj:
                if k in self.keys():
                    if isinstance(self[k], list) and isinstance(obj[k], list):
                        self[k] += obj[k]
                    elif isinstance(self[k], list):
                        self[k].append(obj[k])
                    elif isinstance(obj[k], list):
                        self[k] = [self[k]] + obj[k]
                    elif isinstance(self[k], Config) and isinstance(obj[k], Config):
                        self[k].merge(obj[k])
                    elif isinstance(self[k], Config) and isinstance(obj[k], dict):
                        self[k].merge(obj[k])
                    else:
                        self[k] = [self[k], obj[k]]
                else:
                    if isinstance(obj[k], dict):
                        self[k] = Config(obj[k])
                    else:
                        self[k] = obj[k]
        return self

    def replace_variables(self, variables):
        """ replaces all variables in the config with the given variables"""
        for k, obj in self.items():
            if isinstance(obj, Config):
                obj.replace_variables(variables)
            elif isinstance(obj, str):
                self[k] = obj.format(**variables)
            elif isinstance(obj, list) or isinstance(obj, tuple):
                self[k] = self.replace_in_list(obj, variables)

    def replace_in_list(self, obj, variables):
        """ replaces all variables in the list with the given variables"""
        for i, entry in enumerate(obj):
            if isinstance(entry, Config):
                entry.replace_variables(variables)
            elif isinstance(entry, str):
                obj[i] = entry.format(**variables)
            elif isinstance(obj, list) or isinstance(obj, tuple):
                self.replace_in_list(obj, variables)
        return obj



# def test01():
#     """Test Config class"""
#     class UObject(Config):
#         """Test class"""

#     obj = Config({1: 2})
#     d = {}
#     d.update({
#         "a": 1,
#         "b": {
#             "c": 2,
#             "d": [3, 4, 5],
#             "e": [[6, 7], (8, 9)],
#             "self": d,
#         },
#         1: 10,
#         "1": 11,
#         "obj": obj,
#     })
#     x = UObject(d)
#     print(x)

#     assert x.a == x["a"] == 1
#     assert x.b.c == x["b"]["c"] == 2
#     assert x.b.d[0] == 3
#     assert x.b.d[1] == 4
#     assert x.b.e[0][0] == 6
#     assert x.b.e[1][0] == 8
#     assert x[1] == 10
#     assert x["1"] == 11
#     assert x[1] != x["1"]
#     assert id(x) == id(x.b.self.b.self) == id(x.b.self)
#     assert x.b.self.a == x.b.self.b.self.a == 1

#     x.x = 12
#     assert x.x == x["x"] == 12
#     x.y = {"a": 13, "b": [14, 15]}
#     assert x.y.a == 13
#     assert x.y.b[0] == 14


# def test02():
#     """Test Config class"""
#     x = Config({
#         "a": {
#             "b": 1,
#             "c": [2, 3]
#         },
#         1: 6,
#         2: [8, 9],
#         3: 11,
#     })
#     y = Config({
#         "a": {
#             "b": 4,
#             "c": [5]
#         },
#         1: 7,
#         2: 10,
#         3: [12, 13],
#     })
#     z = {
#         3: 14,
#         2: 15,
#         "a": {
#             "b": 16,
#             "c": 17,
#         }
#     }
#     x.merge(y, z)
#     assert 2 in x.a.c
#     assert 3 in x.a.c
#     assert 5 in x.a.c
#     assert 1 in x.a.b
#     assert 4 in x.a.b
#     assert 8 in x[2]
#     assert 9 in x[2]
#     assert 10 in x[2]
#     assert 11 in x[3]
#     assert 12 in x[3]
#     assert 13 in x[3]
#     assert 14 in x[3]
#     assert 15 in x[2]
#     assert 16 in x.a.b
#     assert 17 in x.a.c


# def test03():
#     """Test Config class"""
#     variables = {"name": "robert", "age": 23}
#     x = Config({
#         "person": {
#             "name": "{name}",
#             "age": "{age}"
#         },
#         "desc": "{name} is of age {age}",
#         "lst1": ["{name}", "{age}"],
#         "lst2": ["{name}", "{age}"]
#     })
#     x.replace_variables(variables)
#     print(x)

# if __name__ == '__main__':
#     test01()
#     test02()
#     test03()
