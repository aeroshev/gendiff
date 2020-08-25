from abc import ABC, abstractmethod
import configparser


class AbstractCONFIG(ABC):

    def __init__(self):
        self.parser = configparser.ConfigParser()

    def read(self, data: str):
        return self.parser.read(data)

    def compare(self):
        pass

    @abstractmethod
    def render(self):
        pass


class PlainCONFIG(AbstractCONFIG):

    def render(self):
        pass


class NestedCONFIG(AbstractCONFIG):

    def render(self):
        pass
