class Component:

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
        if self.param == other.param and self.state == other.state and self.value == other.value:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.param) + hash(self.state)
