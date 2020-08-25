from abc import ABC, abstractmethod

from gendiff.products.product_json import PlainJSON, NestedJSON
from gendiff.products.product_yaml import PlainYAML, NestedYAML
from gendiff.products.product_config import PlainCONFIG, NestedCONFIG


class AbstractFactory(ABC):

    @abstractmethod
    def create_plain(self):
        pass

    @abstractmethod
    def create_nested(self):
        pass


class FactoryJSON(AbstractFactory):
    pass

class FactoryYAML(AbstractFactory):
    pass

class FactoryCONFIG()



class FactoryPlain(AbstractFactory):

    def create_json(self) -> PlainJSON:
        return PlainJSON()

    def create_yaml(self) -> PlainYAML:
        return PlainYAML()

    def create_config(self) -> PlainCONFIG:
        return PlainCONFIG()
