from abc import ABC, abstractmethod
import json
from colorama import init, Fore
from gendiff.generator_ast.components import Component


class AbstractJSON(ABC):

    def read(self, data: str):
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
        # for item_1, item_2 in input_1_json, input_2_json:
            # 1 = 2 = 3 = 4 <-> nothing
            # 1 = 3, 2 = 4 <-> nothing
            # 1 = 3, 2 != 4 <-> update item 2
            # 1 != 3 <-> update item 1, if dict update children
            # 2 - None 4 - object <-> insert item 2
            # 2 = 4, 1 = None, 3 - object <-> delete item 1

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

    def research(self, object_, parent: Component):
        if not isinstance(object_, (list, dict)):
            parent.add(Leaf(object_))
            return
        else:
            if isinstance(object_, list):
                for node in object_:
                    node_ = Composite('list', len(object_))
                    parent.add(node_)
                    self.research(node, node_)
            elif isinstance(object_, dict):
                for key, value in object_.items():
                    if isinstance(value, dict):
                        node = Composite('dict', key)
                        parent.add(node)
                        self.research(value, node)
                    elif isinstance(value, list):
                        list_value = '['
                        list_value += ' '.join([f'{elem}, ' for elem in value])
                        list_value += ']'
                        self.research(f'{key}: {list_value}', parent)
                    else:
                        self.research(f'{key}: {value}', parent)
            else:
                raise TypeError

    @abstractmethod
    def render(self, result):
        pass


class PlainJSON(AbstractJSON):

    def render(self, result):
        pass


class JsonJSON(AbstractJSON):

    def __init__(self):
        self.color = Fore.WHITE
        self.deep = 0
        self.ast = set()
        init()

    def render(self, result):
        status = {'$insert', '$update', '$delete'}

        for key, value in result.items():
            if str(key) in status:
                if str(key) == '$insert':
                    if isinstance(value, dict):
                        self.deep += 1
                        self.color = 'green'
                        self.render(value)
                        self.deep -= 1
                    else:
                        print(self.deep*' ' + f'{Fore.GREEN}+ {value}')
                elif str(key) == '$delete':
                    if isinstance(value, dict):
                        self.deep += 1
                        self.color = 'red'
                        self.render(value)
                        self.deep -= 1
                    else:
                        print(self.deep * ' ' + f'{Fore.RED}- {value}')
            else:
                if isinstance(value, list):
                    print(self.deep*' ' + f'{Fore.RED}- {key}: {value[0]}')
                    print(self.deep*' ' + f'{Fore.GREEN}+ {key}: {value[1]}')
                elif isinstance(value, dict):
                    print(self.deep*' ' + f'{Fore.WHITE}{key}: ' + '{')
                    self.deep += 1
                    self.render(value)
                    self.deep -= 1
                    print(Fore.WHITE + self.deep*' ' + '}')
                else:
                    if self.color == 'green':
                        print(self.deep*' ' + f'{Fore.GREEN}+ {key}: {value}')
                    elif self.color == 'red':
                        print(self.deep * ' ' + f'{Fore.RED}- {key}: {value}')
        print(Fore.WHITE, end='')
