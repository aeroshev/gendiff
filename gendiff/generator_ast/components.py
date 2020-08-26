"""
Содержит в себе класс Component необходимый для построения AST дерева
"""


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

    def __init__(self, param='default', state='default', value='default'):
        self.param = param
        self.state = state
        self.value = value

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
