from abc import ABC, abstractmethod
import json
from colorama import init, Fore
from gendiff.generator_ast.components import Component, Composite, Leaf
from jsondiff import diff


class AbstractJSON(ABC):

    def read(self, data: str):
        return json.loads(data)

    def compare(self, input_1_json, input_2_json):
        return diff(input_1_json, input_2_json, syntax='symmetric')

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
