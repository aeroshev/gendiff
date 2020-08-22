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
    def research(self, object_):
        pass


class PlainJSON(AbstractJSON):

    def read(self, data: str):
        pass

    def compare(self, input_1, input_2):
        pass

    def research(self, object_):
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

    def research(self, object_):
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
        gen = GeneratorAST()
        root = gen.add_node(None, Node('root', []))

        if not isinstance(object_, (list, dict)):
            gen.add_node(root, Node(object_, []))
            return
        else:
            if isinstance(object_, list):
                for node in object_:
                    self.research(node)
            elif isinstance(object_, dict):
                for key, value in object_.items():
                    self.research(str(key) + ': ' + str(value))
            else:
                raise TypeError
