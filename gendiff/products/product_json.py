from abc import ABC, abstractmethod
import json
from itertools import tee
from copy import copy

from gendiff.generator_ast.generator_ast import GeneratorAST, Node


class AbstractJSON(ABC):

    @abstractmethod
    def read(self, data: str):
        pass

    @abstractmethod
    def compare(self, input_1, input_2):
        pass

    @abstractmethod
    def research(self, object_, root, gen):
        pass

    @abstractmethod
    def render(self):
        pass


class PlainJSON(AbstractJSON):

    def read(self, data: str):
        pass

    def compare(self, input_1, input_2):
        pass

    def research(self, object_, root, gen):
        pass

    def render(self):
        pass


class JsonJSON(AbstractJSON):

    def read(self, data: str):
        self.data = json.loads(data)
        return self.data

    # TODO
    def compare(self, input_1: GeneratorAST, input_2: GeneratorAST) -> GeneratorAST:
        diff_tree = GeneratorAST()
        root = diff_tree.add_node(None, Node('root', []))

        self.leaf_1 = input_1.pre_order(input_1.tree)
        self.help_1 = input_1.pre_order(input_1.tree)

        self.leaf_2 = input_2.pre_order(input_2.tree)
        self.help_2 = input_2.pre_order(input_2.tree)

        self.stop_before = False
        self.stop_after = False

        self.loop_shit(root, diff_tree)

        return diff_tree

    def loop_shit(self, current, diff_tree):
        try:
            while True:
                data_1 = next(self.leaf_1)
                data_2 = next(self.leaf_2)

                if not self.stop_before:
                    next(self.help_1)
                if not self.stop_after:
                    next(self.help_2)
                self.stop_before = False
                self.stop_after = False

                if data_1.content != data_2.content:
                    help_data_1 = next(self.help_1)
                    help_data_2 = next(self.help_2)

                    if data_2.content == help_data_1.content:
                        diff_tree.add_node(current, Node(f'- {data_1.content}', []))
                        self.stop_after = True
                        next(self.leaf_1)
                    elif data_1.content == help_data_2.content:
                        diff_tree.add_node(current, Node(f'+ {data_2.content}', []))
                        self.stop_before = True
                        next(self.leaf_2)
                    elif data_1.content.split(':')[0] == data_2.content.split(':')[0]:
                        diff_tree.add_node(current, Node(f'- {data_1.content}\n+ {data_2.content}', []))
                        self.stop_after = True
                        self.stop_before = True
        except StopIteration:
            pass

    def research(self, object_, root, gen):
        if not isinstance(object_, (list, dict)):
            gen.add_node(root, Node(object_, []))
            return
        else:
            if isinstance(object_, list):
                for node in object_:
                    parent = gen.add_node(root, Node('list', []))
                    self.research(node, parent, gen)
            elif isinstance(object_, dict):
                for key, value in object_.items():
                    if isinstance(value, dict):
                        parent = gen.add_node(root, Node(f'{key}-{len(value)}', []))
                        self.research(value, parent, gen)
                    elif isinstance(value, list):
                        list_value = '['
                        list_value += ' '.join([f'{elem}, ' for elem in value])
                        list_value += ']'
                        self.research(f'{key}: {list_value}', root, gen)
                    else:
                        self.research(f'{key}: {value}', root, gen)
            else:
                raise TypeError

    def render(self):
        pass
