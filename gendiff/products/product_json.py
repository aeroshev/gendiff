from abc import ABC, abstractmethod
import json
from colorama import init, Fore
from gendiff.generator_ast.components import Component


class AbstractJSON(ABC):

    @staticmethod
    def read(data: str):
        return json.loads(data)

    def compare(self, input_1_json, input_2_json):
        iter_1 = iter(input_1_json)
        iter_2 = iter(input_2_json)

        while True:
            broke = 0
            try:
                item_1 = next(iter_1)
            except StopIteration:
                broke += 1
            try:
                item_2 = next(iter_2)
            except StopIteration:
                broke += 1
            if broke == 2:
                break
            # 2 - None, 4 - object <-> insert item 2
            # 2 - object, 4 - object <-> update item 2

            # 1 - None, 3 - object <-> delete item 1
            # 1 - object, 3 - object <-> update item 1

            old_in_new = input_2_json.get(item_1)  # 1
            new_in_old = input_1_json.get(item_2)  # 2
            old_in_old = input_1_json.get(item_1)  # 3
            # new_in_new = input_2_json.get(item_2)  # 4

            if new_in_old is None:
                self.ast.add(Component(item_2, 'insert', input_2_json[item_2]))
            if old_in_new is None:
                self.ast.add(Component(item_1, 'delete', input_1_json[item_1]))
            if not (old_in_new is None) and not (old_in_old is None) and old_in_new != old_in_old:
                if isinstance(old_in_old, dict) and isinstance(old_in_new, dict):
                    store = self.ast
                    self.ast = set()
                    new_ = self.compare(old_in_old, old_in_new)
                    self.ast = store
                    object_ = Component(item_1, 'children', new_)
                    if object_ not in self.ast:
                        self.ast.add(object_)
                else:
                    object_ = Component(item_1, 'update', (old_in_old, old_in_new))
                    if object_ not in self.ast:
                        self.ast.add(object_)

        return self.ast

    @abstractmethod
    def render(self, result):
        pass


class PlainJSON(AbstractJSON):

    __slots__ = 'ast'

    def __init__(self):
        self.ast = set()
        init()

    def render(self, result):
        complex_value = '[complex value]'
        for item in result:
            if item.state == 'insert':
                print(f'{Fore.WHITE}Property {Fore.GREEN}\'{item.param}\'{Fore.WHITE} was added with value: '
                      f'{Fore.GREEN}{complex_value if isinstance(item.value, dict) else item.value}')
            elif item.state == 'delete':
                print(f'{Fore.WHITE}Property {Fore.RED}\'{item.param}\'{Fore.WHITE} was removed')
            elif item.state == 'update':
                print(f'{Fore.WHITE}Property {Fore.YELLOW}\'{item.param}\'{Fore.WHITE} was updated. From '
                      f'{Fore.RED}{complex_value if isinstance(item.value[0], dict) else item.value[0]} '
                      f'{Fore.WHITE}to '
                      f'{Fore.GREEN}{complex_value if isinstance(item.value[1], dict) else item.value[1]}')
            elif item.state == 'children':
                self.render(item.value)
            else:
                raise TypeError
        print(f'{Fore.WHITE}', end='')


class JsonJSON(AbstractJSON):

    __slots__ = ('deep', 'ast')

    def __init__(self):
        self.deep = 0
        self.ast = set()
        init()

    def render(self, result: set):
        for item in result:
            if item.state == 'insert':
                print(self.deep*' ' + f'{Fore.GREEN}+ {item.param}: {item.value}')
            elif item.state == 'delete':
                print(self.deep*' ' + f'{Fore.RED}- {item.param}: {item.value}')
            elif item.state == 'update':
                print(self.deep*' ' + f'{Fore.RED}- {item.param}: {item.value[0]}')
                print(self.deep*' ' + f'{Fore.GREEN}+ {item.param}: {item.value[1]}')
            elif item.state == 'children':
                print(Fore.WHITE + self.deep*' ' + f'{item.param}: ' + '{')

                self.deep += 1
                self.render(item.value)
                self.deep -= 1

                print(Fore.WHITE + self.deep*' ' + '}')
            else:
                raise TypeError
        print(f'{Fore.WHITE}', end='')
