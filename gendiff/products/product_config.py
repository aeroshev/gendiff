"""
Этот модуль содержит в себе продукты типа INI
Различие этих классов заключается в разном
типе рендеринга результата
Все общие методы для обоих классов определены
в абстрактном классе
"""
import configparser
from io import TextIOWrapper
from abc import abstractmethod
from typing import Any, Dict, Set

from gendiff.products.abstract_product import AbstractProduct
from gendiff.generator_ast.components import Component


class AbstractCONFIG(AbstractProduct):
    """
    Абстрактный класс семейства продуктов INI
    Определяет в себе общие методы для всех наследников и
    асбтрактные методы, которые необходимо переопределить
    для различных продуктов
    """
    def read(self, file: TextIOWrapper) -> Dict[str, Any]:
        """
        Десериализация строковых данных в python формат
        :param file: данные из файла
        :return: словарик словариков
        """
        returning_dict: Dict[str, Any] = {}
        parser = configparser.ConfigParser()

        parser.read(file.name)
        for section in parser.sections():
            returning_dict.update({section: {}})
            for key in parser[section]:
                returning_dict[section].update({key: parser[section][key]})
        return returning_dict

    @abstractmethod
    def render(self, result: Set[Component]) -> None:
        """
        Вывод различий в терминал пользавателю
        В каждом классе определяется свой стиль
        :param result: AST различий
        :return:
        """


class PlainCONFIG(AbstractCONFIG):
    """
    Класс переопределяющий метод render для плоского вывода результат
    """
    def render(self, result: Set[Component]) -> None:
        pass


class NestedCONFIG(AbstractCONFIG):
    """
    Класс переопределяющий метод render для вложенного вывода результат
    """
    def render(self, result: Set[Component]) -> None:
        pass
