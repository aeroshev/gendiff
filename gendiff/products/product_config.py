"""
Этот модуль содержит в себе продукты типа INI
Различие этих классов заключается в разном
типе рендеринга результата
Все общие методы для обоих классов определены
в абстрактном классе
"""
import configparser
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
    def __init__(self):
        self.parser = configparser.ConfigParser()

    def read(self, data: str) -> Dict[str, Any]:
        """
        Десериализация строковых данных в python формат
        :param data: данные из файла
        :return: словарик словариков
        """
        parser = configparser.ConfigParser()
        parser.read(data)
        return {'Hello': 'world'}

    def compare(self,
                input_1_ini: Dict[str, Any],
                input_2_ini: Dict[str, Any]) -> Set[Component]:
        """
        Главная функция построения AST различий файлов
        Имеет рекусривный вызов для вложенных структур
        :param input_1_ini: десериализованые данные из первого файла
        :param input_2_ini: десериализованые данные из второго файла
        :return: множество Component
        """

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
