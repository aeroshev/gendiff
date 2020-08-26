"""
Содержит в себе класс Component необходимый для построения AST дерева
"""
from typing import Union
from enum import Enum, unique


@unique
class ComponentState(Enum):
    DEFAULT = 1
    INSERT = 2
    DELETE = 3
    UPDATE = 4
    CHILDREN = 5


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

    def __init__(self, param='default', state=ComponentState.DEFAULT, value='default'):
        self.param: str = param
        self.state: ComponentState = state
        self.value: Union[str, dict, set, tuple] = value

    def __str__(self):
        return f'{self.param}, {self.state}, {self.value}'

    def __repr__(self):
        return f'{self.param}, {self.state}, {self.value}'

    def __eq__(self, other):
        status = False
        if self.param == other.param and self.state == other.state and self.value == other.value:
            status = True
        return status

    def __hash__(self):
        return hash(self.param) + hash(self.state)
