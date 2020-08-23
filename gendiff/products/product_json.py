from abc import ABC, abstractmethod
import json

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


class PlainJSON(AbstractJSON):

    def read(self, data: str):
        pass

    def compare(self, input_1, input_2):
        pass

    def research(self, object_, root, gen):
        pass


class JsonJSON(AbstractJSON):

    def read(self, data: str):
        self.data = json.loads(data)
        return self.data

    def compare(self, input_1, input_2):
        gen = GeneratorAST()
        root = gen.add_node(None, Node('root', []))

        for value_1, value_2 in zip(self.research(input_1), self.research(input_2)):
            if value_1 != value_2:
               pass

    def research(self, object_, root, gen):
        # if not isinstance(object_, (list, dict)):
        #     yield object_
        # else:
        #     if isinstance(object_, list):
        #         for node in object_:
        #             for x in self.research(node):
        #                 yield x
        #     elif isinstance(object_, dict):
        #         for key in object_.keys():
        #             for x in self.research(object_[key]):
        #                 yield x
        #     else:
        #         raise TypeError

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
                        parent = gen.add_node(root, Node(key, []))
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
