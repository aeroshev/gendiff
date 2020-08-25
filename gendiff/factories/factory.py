from abc import ABC, abstractmethod

from gendiff.products.product_json import PlainJSON, NestedJSON
from gendiff.products.product_yaml import PlainYAML, NestedYAML
from gendiff.products.product_config import PlainCONFIG, NestedCONFIG


class AbstractFactory(ABC):

    @abstractmethod
    def create_nested(self):
        pass

    @abstractmethod
    def create_plain(self):
        pass


class FactoryJSON(AbstractFactory):

    def create_plain(self) -> PlainJSON:
        return PlainJSON()

    def create_nested(self) -> NestedJSON:
        return NestedJSON()


class FactoryYAML(AbstractFactory):

    def create_plain(self) -> PlainYAML:
        return PlainYAML()

    def create_nested(self) -> NestedYAML:
        return NestedYAML()


class FactoryCONFIG(AbstractFactory):

    def create_plain(self) -> PlainCONFIG:
        return PlainCONFIG()

    def create_nested(self) -> NestedCONFIG:
        return NestedCONFIG()
