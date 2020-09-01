"""
Этот модуль содержит в себе общий класс для всех продуктов
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Set

from gendiff.generator_ast.components import Component


class AbstractProduct(ABC):
    """
    Этот класс является главным предком для всех продуктов.
    Через него определяются общие интерфейсы для всех
    наследников
    """
    @abstractmethod
    def read(self, data: str) -> Dict[str, Any]:
        """
        Функция десериализации данных, которая
        оссобенна для каждого формата
        :param data:
        :return:
        """

    @abstractmethod
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

    @abstractmethod
    def render(self, result: Set[Component]) -> None:
        """
        Представление пользователю
        оформленного отчёта о
        найденных различиях
        :param result:
        :return:
        """
