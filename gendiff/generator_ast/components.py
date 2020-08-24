from abc import ABC, abstractmethod


class Component(ABC):

    __slots__ = ('parent', 'type', 'data')

    @abstractmethod
    def is_composite(self) -> bool:
        pass

    def __str__(self):
        return str(self.data)

    def add(self, component) -> None:
        pass

    def remove(self, component) -> None:
        pass

    @abstractmethod
    def is_root(self) -> bool:
        pass

    def pre_order_traversal(self, component, deep):
        if not component.is_composite():
            print('  ' * deep + str(component))
            return
        if component.type == 'list':
            print('  ' * deep + '[')
        elif component.type == 'dict':
            print('  ' * deep + str(component) + ': {')
        deep += 1
        for child in component.children:
            self.pre_order_traversal(child, deep)

        deep -= 1
        if component.type == 'list':
            print('  ' * deep + ']')
        elif component.type == 'dict':
            print('  ' * deep + '}')

    def pre_order_traversal_generator(self, component):
        if not component.is_composite():
            yield component
            return
        yield component
        for child in component.children:
            for x in self.pre_order_traversal_generator(child):
                yield x


class Composite(Component):

    __slots__ = ('parent', 'type', 'children', 'data')

    def __init__(self, type_, data):
        self.parent = None
        self.type = type_
        self.data = data
        self.children = []

    def is_composite(self) -> bool:
        return True

    def add(self, component: Component) -> None:
        self.children.append(component)
        component.parent = self

    def remove(self, component) -> None:
        self.children.remove(component)
        component.parent = None

    def is_root(self) -> bool:
        return False


class Leaf(Component):

    __slots__ = ('parent', 'type', 'data')

    def __init__(self, data):
        self.parent = None
        self.type = 'leaf'
        self.data = data

    def is_composite(self) -> bool:
        return False

    def is_root(self) -> bool:
        return False


class Root(Component):

    __slots__ = ('parent', 'type', 'children', 'data')

    def __init__(self):
        self.parent = None
        self.type = 'root'
        self.data = 'root'
        self.children = []

    def is_composite(self) -> bool:
        return True

    def is_root(self) -> bool:
        return True

    def add(self, component: Component) -> None:
        self.children.append(component)
        component.parent = self

    def remove(self, component) -> None:
        self.children.remove(component)
        component.parent = None


# TODO write getitem
class WalkerTree:

    __slots__ = ('generator', 'current_node', 'prev_node')

    def __init__(self, root: Component):
        self.generator = root.pre_order_traversal_generator(root)
        self.current_node = next(self.generator)
        self.prev_node = self.current_node

    def __str__(self):
        return str(self.current_node)

    def __iter__(self):
        return self.current_node

    @property
    def data(self):
        return self.current_node.data

    @property
    def type(self):
        return self.current_node.type

    @property
    def prev(self):
        return self.prev_node

    @property
    def itself(self):
        return self.current_node

    def __next__(self):
        self.prev_node = self.current_node
        self.current_node = next(self.generator)
        return self.current_node
