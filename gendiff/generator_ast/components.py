"""
Содержит в себе класс Component необходимый для построения AST дерева
"""
from enum import Enum, unique
from typing import Set, Union


@unique
class ComponentState(Enum):
    INSERT = 1
    DELETE = 2
    UPDATE = 3
    CHILDREN = 4


class Component:
    """
    Этот класс является блоком для составления AST
    В читаемом файле данные сгруппированы как ключ - значение
    param - имя ключа
    state - имеет четыре состояния
        - insert <-> этот блок является новым по отношению к старому файлу
        - delete <-> этот блок был удалён по отношению к старому файлу
        - update <-> этот блок был обновлён по отношению к старому файлу
        - children <-> внутри этого блока произошли изменения
    value - содержит в себе значение ключа
    """

    __slots__ = ('param', 'state', 'value')

    def __init__(self, param, state, value):
        self.param: str = param
        self.state: ComponentState = state
        self.value: Union[Set[Component],
                          bool,
                          int,
                          float,
                          tuple,
                          str] = value

    def __str__(self):
        return f'{self.param}, {self.state}, {self.value}'

    def __repr__(self):
        return f'{self.param}, {self.state}, {self.value}'

    def __eq__(self, other):
        return True if self.param == other.param \
                       and self.state == other.state \
                       and self.value == other.value else False

    def __hash__(self):
        return hash(self.param) + hash(self.state)
