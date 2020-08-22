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


class PlainJSON(AbstractJSON):

    def read(self, data: str):
        pass

    def compare(self, input_1, input_2):
        pass


class JsonJSON(AbstractJSON):

    def read(self, data: str):
        self.data = json.loads(data)
        return self.data

    def compare(self, input_1, input_2):
        if isinstance(input_1, list) and isinstance(input_2, list):
            for chunk_1, chunk_2 in zip(input_1, input_2):
                pass
        elif isinstance(input_1, dict) and isinstance(input_2, dict):
            for key_1, key_2 in zip(input_1.keys(), input_2.keys()):
                pass

    def research(self, object_):
        if not isinstance(object_, (list, dict)):
            yield object_
        else:
            if isinstance(object_, list):
                for node in object_:
                    for x in self.research(node):
                        yield x
            elif isinstance(object_, dict):
                for key in object_.keys():
                    for x in self.research(object_[key]):
                        yield x
            else:
                raise TypeError
