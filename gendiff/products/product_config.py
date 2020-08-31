"""
Этот модуль содержит в себе продукты типа INI
Различие этих классов заключается в разном
типе рендеринга результата
Все общие методы для обоих классов определены
в абстрактном классе
"""
import configparser
from abc import abstractmethod

from gendiff.products.abstract_product import AbstractProduct


class AbstractCONFIG(AbstractProduct):
    """
    Абстрактный класс семейства продуктов INI
    Определяет в себе общие методы для всех наследников и
    асбтрактные методы, которые необходимо переопределить
    для различных продуктов
    """
    def __init__(self):
        self.parser = configparser.ConfigParser()

    def read(self, data: str):
        """
        Десериализация строковых данных в python формат
        :param data: данные из файла
        :return: словарик словариков
        """
        parser = configparser.ConfigParser()
        parser.read(data)

    def compare(self, input_1_ini: dict, input_2_ini: dict):
        """
        Главная функция построения AST различий файлов
        Имеет рекусривный вызов для вложенных структур
        :param input_1_ini: десериализованые данные из первого файла
        :param input_2_ini: десериализованые данные из второго файла
        :return: множество Component
        """

    @abstractmethod
    def render(self, result: set):
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
    def render(self, result: set):
        pass


class NestedCONFIG(AbstractCONFIG):
    """
    Класс переопределяющий метод render для вложенного вывода результат
    """
    def render(self, result: set):
        pass
