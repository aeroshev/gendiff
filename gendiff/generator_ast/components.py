"""
Содержит в себе класс Component необходимый для построения AST дерева
"""
from enum import Enum, unique
from typing import Set, Union, Any


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

    def __init__(self, param: str, state: ComponentState, value: Any) -> None:
        self.param: str = param
        self.state: ComponentState = state
        self.value: Union[Set[Component], Any] = value

    def __str__(self) -> str:
        return f'{self.param}, {self.state}, {self.value}'

    def __repr__(self) -> str:
        return f'{self.param}, {self.state}, {self.value}'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Component):
            return NotImplemented
        return True if self.param == other.param \
                       and self.state == other.state \
                       and self.value == other.value else False

    def __hash__(self) -> int:
        return hash(self.param) + hash(self.state)
