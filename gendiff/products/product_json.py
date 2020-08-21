from abc import ABC, abstractmethod
import json

from gendiff.generator_ast.generator_ast import GeneratorAST, Node


class AbstractJSON(ABC):

    @staticmethod
    def read(data: str):
        pass

    @abstractmethod
    def compare(self, input_1, input_2):
        pass


class PlainJSON(AbstractJSON):

    @staticmethod
    def read(data: str):
        pass

    def compare(self, input_1, input_2):
        pass


class JsonJSON(AbstractJSON):

    @staticmethod
    def read(data: str):
        output = json.loads(data)
        return output

    def compare(self, input_1, input_2):
        if isinstance(input_1, list) and isinstance(input_2, list):
            for chunk_1, chunk_2 in zip(input_1, input_2):
                pass
        elif isinstance(input_1, dict) and isinstance(input_2, dict):
            for key_1, key_2 in zip(input_1.keys(), input_2.keys()):
                pass
