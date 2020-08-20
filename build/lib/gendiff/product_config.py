from abc import ABC, abstractmethod


class AbstractCONFIG(ABC):

    @abstractmethod
    def read(self):
        pass


class PlainCONFIG(AbstractCONFIG):

    def read(self):
        pass
