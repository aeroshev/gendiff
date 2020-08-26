"""
Этот модуль содержит в себе продукты типа INI
Различие этих классов заключается в разном
типе рендеринга результата
Все общие методы для обоих классов определены
в абстрактном классе
"""
from abc import ABC, abstractmethod
import configparser


class AbstractCONFIG(ABC):
    """
    Абстрактный класс семейства продуктов INI
    Определяет в себе общие методы для всех наследников и
    асбтрактные методы, которые необходимо переопределить
    для различных продуктов
    """
    def __init__(self):
        self.parser = configparser.ConfigParser()

    @staticmethod
    def read(data: str):
        """
        Десериализация строковых данных в python формат
        :param data: данные из файла
        :return: словарик словариков
        """
        parser = configparser.ConfigParser()
        parser.read(data)

    def compare(self):
        """
        Главная функция построения AST различий файлов
        Имеет рекусривный вызов для вложенных структур
        :param input_1_yaml: десериализованые данные из первого файла
        :param input_2_yaml: десериализованые данные из второго файла
        :return: множество Component
        """

    @abstractmethod
    def render(self):
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
    def render(self):
        pass


class NestedCONFIG(AbstractCONFIG):
    """
    Класс переопределяющий метод render для вложенного вывода результат
    """
    def render(self):
        pass
