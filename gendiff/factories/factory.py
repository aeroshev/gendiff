from abc import ABC

from gendiff.products.product_json import PlainJSON, JsonJSON
from gendiff.products.product_yaml import PlainYAML, JsonYAML
from gendiff.products.product_config import PlainCONFIG, JsonCONFIG


class AbstractFactory(ABC):

    @staticmethod
    def create_plain():
        pass

    @staticmethod
    def create_json():
        pass


class FactoryJSON(AbstractFactory):

    @staticmethod
    def create_plain() -> PlainJSON:
        return PlainJSON()

    @staticmethod
    def create_json() -> JsonJSON:
        return JsonJSON()


class FactoryYAML(AbstractFactory):

    @staticmethod
    def create_plain() -> PlainYAML:
        return PlainYAML()

    @staticmethod
    def create_json() -> JsonYAML:
        return JsonYAML()


class FactoryCONFIG(AbstractFactory):

    @staticmethod
    def create_plain() -> PlainCONFIG:
        return PlainCONFIG()

    @staticmethod
    def create_json() -> JsonCONFIG:
        return JsonCONFIG()
