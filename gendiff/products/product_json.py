from abc import ABC, abstractmethod
import json


class AbstractJSON(ABC):

    @staticmethod
    def read(data: str):
        pass

    @staticmethod
    def compare(input_1, input_2):
        pass


class PlainJSON(AbstractJSON):

    @staticmethod
    def read(data: str):
        pass

    @staticmethod
    def compare(input_1, input_2):
        pass


class JsonJSON(AbstractJSON):

    @staticmethod
    def read(data: str):
        output = json.loads(data)
        return output

    @staticmethod
    def compare(input_1, input_2):
        pass
