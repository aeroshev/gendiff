from abc import ABC, abstractmethod

from gendiff.products.product_json import PlainJSON, NestedJSON
from gendiff.products.product_yaml import PlainYAML, NestedYAML
from gendiff.products.product_config import PlainCONFIG, NestedCONFIG


class AbstractFactory(ABC):

    @abstractmethod
    def create_json(self):
        pass

    @abstractmethod
    def create_yaml(self):
        pass

    @abstractmethod
    def create_config(self):
        pass


class FactoryNested(AbstractFactory):

    def create_json(self) -> NestedJSON:
        return NestedJSON()

    def create_yaml(self) -> NestedYAML:
        return NestedYAML()

    def create_config(self) -> NestedCONFIG:
        return NestedCONFIG()


class FactoryPlain(AbstractFactory):

    def create_json(self) -> PlainJSON:
        return PlainJSON()

    def create_yaml(self) -> PlainYAML:
        return PlainYAML()

    def create_config(self) -> PlainCONFIG:
        return PlainCONFIG()
