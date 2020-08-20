from abc import ABC, abstractmethod


class AbstractJSON(ABC):

    @abstractmethod
    def read(self):
        pass

    @staticmethod
    def compare(input_1, input_2):
        pass


class PlainJSON(AbstractJSON):

    def read(self):
        pass

    @staticmethod
    def compare(input_1, input_2):
        pass
