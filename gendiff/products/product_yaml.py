"""
Этот модуль содержит в себе продукты типа YAML
Различие этих классов заключается в разном
типе рендеринга результата
Все общие методы для обоих классов определены
в абстрактном классе
"""
from abc import abstractmethod
from io import TextIOWrapper
from typing import Any, Dict, List, Set

import yaml
from gendiff.generator_ast.components import Component, ComponentState
from gendiff.products.abstract_product import AbstractProduct


class AbstractYAML(AbstractProduct):
    """
    Абстрактный класс семейства продуктов YAML
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
        data = yaml.load(file, yaml.Loader)
        if isinstance(data, dict):
            return data
        else:
            raise SystemError

    @abstractmethod
    def dirty_render(self, result: Set[Component]) -> str:
        """
        Вывод различий в терминал пользавателю
        В каждом классе определяется свой стиль
        :param result: AST различий
        :return:
        """


class PlainYAML(AbstractYAML):
    """
    Класс переопределяющий метод render для плоского вывода результат
    """
    __slots__ = ('ast', 'path', 'report', 'paint')

    def __init__(self) -> None:
        super().__init__()
        self.path: List[str] = []

    @staticmethod
    def is_complex(value: Any) -> str:
        return '[complex value]' if isinstance(value, dict) else str(value)

    def dirty_render(self, result: Set[Component]) -> str:
        for item in result:
            self.path.append(item.param)
            if item.state == ComponentState.INSERT:
                self.report += f'{self.paint.SIMPLE}Property '\
                               f'{self.paint.INSERT}\'' \
                               f'{".".join(self.path)}\''\
                               f'{self.paint.SIMPLE} was added with value: '\
                               f'{self.paint.INSERT}'\
                               f'{self.is_complex(item.value)}\n'
            elif item.state == ComponentState.DELETE:
                self.report += f'{self.paint.SIMPLE}Property '\
                               f'{self.paint.DELETE}\'' \
                               f'{".".join(self.path)}\''\
                               f'{self.paint.SIMPLE} was removed\n'
            elif item.state == ComponentState.UPDATE:
                if isinstance(item.value, tuple):
                    self.report += f'{self.paint.SIMPLE}Property '\
                                   f'{self.paint.UPDATE}\'' \
                                   f'{".".join(self.path)}\''\
                                   f'{self.paint.SIMPLE} '\
                                   f'was updated. From '\
                                   f'{self.paint.DELETE}'\
                                   f'{self.is_complex(item.value[0])} '\
                                   f'{self.paint.SIMPLE}to '\
                                   f'{self.paint.INSERT}'\
                                   f'{self.is_complex(item.value[1])}\n'
                else:
                    raise TypeError
            elif item.state == ComponentState.CHILDREN:
                if isinstance(item.value, set):
                    self.dirty_render(item.value)
                else:
                    raise TypeError
            else:
                raise TypeError
            self.path.pop(-1)
        return self.report


class NestedYAML(AbstractYAML):
    """
    Класс переопределяющий метод render для вложенного вывода результат
    """
    __slots__ = ('deep', 'ast')

    def __init__(self) -> None:
        super().__init__()
        self.deep: int = 0

    def decomposition(self, object_: Any) -> str:
        """
        Декомпозиция value из Component словаря
        для pretty print
        :param object_: some value from Component
        :return: pretty string
        """
        if isinstance(object_, dict):
            key, contain = [*object_.items()][0]
            value = '\n' + (self.deep + 4) * ' ' + \
                    f'{key}: {contain}'
        else:
            value = str(object_)
        return value

    def dirty_render(self, result: Set[Component]) -> str:
        for item in result:
            if item.state == ComponentState.INSERT:
                self.report += self.deep * ' ' + \
                               f'{self.paint.INSERT}+ ' \
                               f'{item.param}: '\
                               f'{self.decomposition(item.value)}\n'
            elif item.state == ComponentState.DELETE:
                self.report += self.deep * ' ' + \
                               f'{self.paint.DELETE}- ' \
                               f'{item.param}: '\
                               f'{self.decomposition(item.value)}\n'
            elif item.state == ComponentState.UPDATE:
                if isinstance(item.value, tuple):
                    self.report += self.deep * ' ' + \
                                   f'{self.paint.DELETE}- ' \
                                   f'{item.param}: '\
                                   f'{self.decomposition(item.value[0])}\n' + \
                                   self.deep * ' ' + \
                                   f'{self.paint.INSERT}+ ' \
                                   f'{item.param}: '\
                                   f'{self.decomposition(item.value[1])}\n'
                else:
                    raise TypeError
            elif item.state == ComponentState.CHILDREN:
                if isinstance(item.value, set):
                    self.report += self.paint.SIMPLE + \
                                   self.deep * ' ' + \
                                   f'{item.param}:\n'

                    self.deep += 2
                    self.dirty_render(item.value)
                    self.deep -= 2
                else:
                    raise TypeError
            else:
                raise TypeError
        return self.report
