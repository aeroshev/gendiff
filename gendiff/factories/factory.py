from abc import ABC, abstractmethod

from gendiff.products.product_json import PlainJSON
from gendiff.products.product_yaml import PlainYAML
from gendiff.products.product_config import PlainCONFIG


class AbstractFactory(ABC):

    @staticmethod
    def create_plain():
        pass


class FactoryJSON(AbstractFactory):

    @staticmethod
    def create_plain() -> PlainJSON:
        return PlainJSON()


class FactoryYAML(AbstractFactory):

    @staticmethod
    def create_plain() -> PlainYAML:
        return PlainYAML()


class FactoryCONFIG(AbstractFactory):

    @staticmethod
    def create_plain() -> PlainCONFIG:
        return PlainCONFIG()
