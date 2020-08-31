"""
Этот модуль содержит в себе продукты типа JSON
Различие этих классов заключается в разном
типе рендеринга результата
Все общие методы для обоих классов определены
в абстрактном классе
"""
import json
from abc import abstractmethod
from typing import Any, List, Union, Set

from colorama import Fore, init

from gendiff.generator_ast.components import Component, ComponentState
from gendiff.products.abstract_product import AbstractProduct


class AbstractJSON(AbstractProduct):
    """
    Абстрактный класс семейства продуктов JSON
    Определяет в себе общие методы для всех наследников и
    асбтрактные методы, которые необходимо переопределить
    для различных продуктов
    """
    def __init__(self):
        self.ast: set = set()

    def read(self, data: str) -> dict:
        """
        Десериализация строковых данных в python формат
        :param data: данные из файла
        :return: словарик словариков
        """
        return json.loads(data)

    def compare(self, input_1_json: dict, input_2_json: dict) -> Set[Component]:
        """
        Главная функция построения AST различий файлов
        Имеет рекусривный вызов для вложенных структур
        :param input_1_json: десериализованые данные из первого файла
        :param input_2_json: десериализованые данные из второго файла
        :return: множество Component
        """
        iter_1 = iter(input_1_json)
        iter_2 = iter(input_2_json)

        while True:
            broke = 0
            try:
                item_1 = next(iter_1)
            except StopIteration:
                broke += 1
            try:
                item_2 = next(iter_2)
            except StopIteration:
                broke += 1
            if broke == 2:
                break
            # 2 - None, 4 - object <-> insert item 2
            # 2 - object, 4 - object <-> update item 2

            # 1 - None, 3 - object <-> delete item 1
            # 1 - object, 3 - object <-> update item 1

            old_in_new = input_2_json.get(item_1)  # 1
            new_in_old = input_1_json.get(item_2)  # 2
            old_in_old = input_1_json.get(item_1)  # 3
            # new_in_new = input_2_json.get(item_2)  # 4

            if new_in_old is None:
                self.ast.add(Component(item_2,
                                       ComponentState.INSERT,
                                       input_2_json[item_2]))
            if old_in_new is None:
                self.ast.add(Component(item_1,
                                       ComponentState.DELETE,
                                       input_1_json[item_1]))
            if not (old_in_new is None) \
                    and not (old_in_old is None) \
                    and old_in_new != old_in_old:
                if isinstance(old_in_old, dict) \
                        and isinstance(old_in_new, dict):
                    store = self.ast
                    self.ast = set()
                    new_ = self.compare(old_in_old, old_in_new)
                    self.ast = store
                    object_ = Component(item_1,
                                        ComponentState.CHILDREN,
                                        new_)
                    if object_ not in self.ast:
                        self.ast.add(object_)
                else:
                    object_ = Component(item_1,
                                        ComponentState.UPDATE,
                                        (old_in_old, old_in_new))
                    if object_ not in self.ast:
                        self.ast.add(object_)

        return self.ast

    @abstractmethod
    def render(self, result: set) -> None:
        """
        Вывод различий в терминал пользавателю
        В каждом классе определяется свой стиль
        :param result: AST различий
        :return:
        """


class PlainJSON(AbstractJSON):
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

    def render(self, result: Union[set, dict]) -> None:
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
                print(f'{Fore.WHITE}Property '
                      f'{Fore.YELLOW}\'{".".join(self.path)}\''
                      f'{Fore.WHITE} was updated. From '
                      f'{Fore.RED}'
                      f'{self.is_complex(item.value)} '
                      f'{Fore.WHITE}to '
                      f'{Fore.GREEN}'
                      f'{self.is_complex(item.value[1])}')
            elif item.state == ComponentState.CHILDREN:
                self.render(item.value)
            else:
                raise TypeError
            self.path.pop(-1)
        print(f'{Fore.WHITE}', end='')


class NestedJSON(AbstractJSON):
    """
    Класс переопределяющий метод render для вложенного вывода результат
    """
    __slots__ = ('deep', 'ast')

    def __init__(self):
        super().__init__()
        self.deep: int = 0
        init()

    def decompot(self, object_: Any) -> str:
        """
        Декомпозиция value из Component словаря
        для pretty print
        :param object_: some value from Component
        :return: pretty string
        """
        if isinstance(object_, dict):
            key, contain = [*object_.items()][0]
            value = '{\n' + (self.deep + 1)*' ' + \
                    f'{key}: {contain}\n' + self.deep*' ' + '}'
        else:
            value = str(object_)
        return value

    def render(self, result: Union[set, dict]) -> None:
        for item in result:
            if item.state == ComponentState.INSERT:
                print(self.deep*' ' +
                      f'{Fore.GREEN}+ {item.param}: '
                      f'{self.decompot(item.value)}')
            elif item.state == ComponentState.DELETE:
                print(self.deep*' ' +
                      f'{Fore.RED}- {item.param}: '
                      f'{self.decompot(item.value)}')
            elif item.state == ComponentState.UPDATE:
                print(self.deep*' ' +
                      f'{Fore.RED}- {item.param}: '
                      f'{self.decompot(item.value[0])}')
                print(self.deep*' ' +
                      f'{Fore.GREEN}+ {item.param}: '
                      f'{self.decompot(item.value[1])}')
            elif item.state == ComponentState.CHILDREN:
                print(Fore.WHITE + self.deep*' ' + f'{item.param}: ' + '{')

                self.deep += 1
                self.render(item.value)
                self.deep -= 1

                print(Fore.WHITE + self.deep*' ' + '}')
            else:
                raise TypeError
        print(f'{Fore.WHITE}', end='')
