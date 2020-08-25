from abc import ABC, abstractmethod


class AbstractNested(ABC):

    @abstractmethod
    def read(self):
        pass

    def render(self):
        pass

class NestedJSON(AbstractNested):

class NestedYAML(AbstractNested):

class NestedCONFIG(AbstractNested);