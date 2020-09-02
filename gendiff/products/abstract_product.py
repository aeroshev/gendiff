"""
Этот модуль содержит в себе общий класс для всех продуктов
"""
from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import Any, Dict, Iterator, Set

from gendiff.generator_ast.components import Component, ComponentState


class AbstractProduct(ABC):
    """
    Этот класс является главным предком для всех продуктов.
    Через него определяются общие интерфейсы для всех
    наследников
    """
    def __init__(self):
        self.ast: Set[Component] = set()

    @abstractmethod
    def read(self, file: TextIOWrapper) -> Dict[str, Any]:
        """
        Функция десериализации данных, которая
        оссобенна для каждого формата
        :param file:
        :return:
        """

    def compare(self,
                input_1: Dict[str, Any],
                input_2: Dict[str, Any]) -> Set[Component]:
        """
        Функция сравения двух исходников
        и составление AST дерева.
        Реализация может быть различной в зависимости
        от сериализатора
        :param input_1:
        :param input_2:
        :return:
        """
        iter_1: Iterator = iter(input_1)
        iter_2: Iterator = iter(input_2)

        key_1: str = ''
        key_2: str = ''

        while True:
            broke = 0
            try:
                key_1 = next(iter_1)
            except StopIteration:
                broke += 1
            try:
                key_2 = next(iter_2)
            except StopIteration:
                broke += 1
            if broke == 2:
                break
            # 2 - None, 4 - object <-> insert item 2
            # 2 - object, 4 - object <-> update item 2

            # 1 - None, 3 - object <-> delete item 1
            # 1 - object, 3 - object <-> update item 1

            old_in_new = input_2.get(key_1)  # 1
            new_in_old = input_1.get(key_2)  # 2
            old_in_old = input_1.get(key_1)  # 3
            # new_in_new = input_2_json.get(key_2)  # 4

            if new_in_old is None:
                self.ast.add(Component(key_2,
                                       ComponentState.INSERT,
                                       input_2[key_2]))
            if old_in_new is None:
                self.ast.add(Component(key_1,
                                       ComponentState.DELETE,
                                       input_1[key_1]))
            if not (old_in_new is None) \
                    and not (old_in_old is None) \
                    and old_in_new != old_in_old:
                if isinstance(old_in_old, dict) \
                        and isinstance(old_in_new, dict):
                    store = self.ast
                    self.ast = set()
                    new_ = self.compare(old_in_old, old_in_new)
                    self.ast = store
                    object_ = Component(key_1,
                                        ComponentState.CHILDREN,
                                        new_)
                    if object_ not in self.ast:
                        self.ast.add(object_)
                else:
                    object_ = Component(key_1,
                                        ComponentState.UPDATE,
                                        (old_in_old, old_in_new))
                    if object_ not in self.ast:
                        self.ast.add(object_)

        return self.ast

    @abstractmethod
    def render(self, result: Set[Component]) -> None:
        """
        Представление пользователю
        оформленного отчёта о
        найденных различиях
        :param result:
        :return:
        """
