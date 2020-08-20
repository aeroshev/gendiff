from abc import ABC, abstractmethod


class AbstractJSON(ABC):

    @abstractmethod
    def read(self):
        pass


class PlainJSON(AbstractJSON):

    def read(self):
        pass
