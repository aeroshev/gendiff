class Node:
    __slots__ = ['content', 'children']

    def __init__(self, content, children):
        self.content = content
        self.children = children

    def __str__(self):
        return self.content


class GeneratorAST:
    __slots__ = ['__root']

    def __init__(self):
        self.__root = None

    def add_node(self, parent: Node, new: Node):
        if new is None:
            raise KeyError

        if parent is None and self.__root is None:
            self.__root = new
            return self.__root
        elif parent is None and not (self.__root is None):
            current_node = self.__root
            current_node.children.append(new)
        else:
            current_node = parent
            current_node.children.append(new)

        return current_node.children[-1]

    def pre_order(self, node):
        if node is None:
            return
        yield node
        for child in node.children:
            for x in self.pre_order(child):
                yield x

    @property
    def tree(self):
        return self.__root
