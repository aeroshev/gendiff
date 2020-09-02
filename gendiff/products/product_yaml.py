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
from colorama import Fore, init

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
    def render(self, result: Set[Component]) -> None:
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
    __slots__ = ('ast', 'path')

    def __init__(self):
        super().__init__()
        self.path: List[str] = []
        init()

    @staticmethod
    def is_complex(value: Any) -> str:
        return '[complex value]' if isinstance(value, dict) else str(value)

    def render(self, result: Set[Component]) -> None:
        for item in result:
            self.path.append(item.param)
            if item.state == ComponentState.INSERT:
                print(f'{Fore.WHITE}Property '
                      f'{Fore.GREEN}\'{".".join(self.path)}\''
                      f'{Fore.WHITE} was added with value: '
                      f'{Fore.GREEN}'
                      f'{self.is_complex(item.value)}')
            elif item.state == ComponentState.DELETE:
                print(f'{Fore.WHITE}Property '
                      f'{Fore.RED}\'{".".join(self.path)}\''
                      f'{Fore.WHITE} was removed')
            elif item.state == ComponentState.UPDATE:
                if isinstance(item.value, tuple):
                    print(f'{Fore.WHITE}Property '
                          f'{Fore.YELLOW}\'{".".join(self.path)}\''
                          f'{Fore.WHITE} '
                          f'was updated. From '
                          f'{Fore.RED}'
                          f'{self.is_complex(item.value[0])} '
                          f'{Fore.WHITE}to '
                          f'{Fore.GREEN}'
                          f'{self.is_complex(item.value[1])}')
                else:
                    raise TypeError
            elif item.state == ComponentState.CHILDREN:
                if isinstance(item.value, set):
                    self.render(item.value)
                else:
                    raise TypeError
            else:
                raise TypeError
            self.path.pop(-1)
        print(f'{Fore.WHITE}', end='')


class NestedYAML(AbstractYAML):
    """
    Класс переопределяющий метод render для вложенного вывода результат
    """
    __slots__ = ('deep', 'ast')

    def __init__(self):
        super().__init__()
        self.deep: int = 0
        init()

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

    def render(self, result: Set[Component]) -> None:
        for item in result:
            if item.state == ComponentState.INSERT:
                print(self.deep * ' ' +
                      f'{Fore.GREEN}+ {item.param}: '
                      f'{self.decomposition(item.value)}')
            elif item.state == ComponentState.DELETE:
                print(self.deep * ' ' +
                      f'{Fore.RED}- {item.param}: '
                      f'{self.decomposition(item.value)}')
            elif item.state == ComponentState.UPDATE:
                if isinstance(item.value, tuple):
                    print(self.deep * ' ' +
                          f'{Fore.RED}- {item.param}: '
                          f'{self.decomposition(item.value[0])}')
                    print(self.deep * ' ' +
                          f'{Fore.GREEN}+ {item.param}: '
                          f'{self.decomposition(item.value[1])}')
                else:
                    raise TypeError
            elif item.state == ComponentState.CHILDREN:
                if isinstance(item.value, set):
                    print(Fore.WHITE + self.deep * ' ' + f'{item.param}:')

                    self.deep += 2
                    self.render(item.value)
                    self.deep -= 2
                else:
                    raise TypeError
            else:
                raise TypeError
        print(f'{Fore.WHITE}', end='')
