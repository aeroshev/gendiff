from abc import ABC, abstractmethod


class AbstractYAML(ABC):

    @abstractmethod
    def read(self):
        pass


class PlainYAML(AbstractYAML):

    def read(self):
        pass


class JsonYAML(AbstractYAML):

    def read(self):
        pass
