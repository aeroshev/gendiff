"""
Это модуль содержит в себе фабрики двух семейств:
NestedFactory - печать результата в родном стиле файла
PlainFactory - печать результата в плоском стиле
"""
from abc import ABC, abstractmethod

from gendiff.products.product_json import PlainJSON, NestedJSON
from gendiff.products.product_yaml import PlainYAML, NestedYAML
from gendiff.products.product_config import PlainCONFIG, NestedCONFIG


class AbstractFactory(ABC):
    """
    Абстрактный класс, который обеспечивает единый интерфейс
    для всех фабрик
    """
    @abstractmethod
    def create_json(self):
        """
        Возращает продукт для обработки JSON файлов
        :return:
        """

    @abstractmethod
    def create_yaml(self):
        """
        Возращает продукт для обработки YAML файлов
        :return:
        """

    @abstractmethod
    def create_config(self):
        """
        Возращает продукт для обработки INI файлов
        :return:
        """


class FactoryNested(AbstractFactory):
    """
    Фабрика семейства Nested
    """
    def create_json(self) -> NestedJSON:
        return NestedJSON()

    def create_yaml(self) -> NestedYAML:
        return NestedYAML()

    def create_config(self) -> NestedCONFIG:
        return NestedCONFIG()


class FactoryPlain(AbstractFactory):
    """
    Фабрика семейства Plain
    """
    def create_json(self) -> PlainJSON:
        return PlainJSON()

    def create_yaml(self) -> PlainYAML:
        return PlainYAML()

    def create_config(self) -> PlainCONFIG:
        return PlainCONFIG()
