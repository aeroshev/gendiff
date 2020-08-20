from abc import ABC, abstractmethod

from gendiff.products.product_json import PlainJSON
from gendiff.products.product_yaml import PlainYAML
from gendiff.products.product_config import PlainCONFIG


class AbstractFactory(ABC):

    @abstractmethod
    def create_plain(self):
        pass


class FactoryJson(AbstractFactory):

    def create_plain(self):
        return PlainJSON()


class FactoryYAML(AbstractFactory):

    def create_plain(self):
        return PlainYAML


class FactoryCONFIG(AbstractFactory):

    def create_plain(self):
        return PlainCONFIG
