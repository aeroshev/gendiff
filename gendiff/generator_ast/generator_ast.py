class Node:

    def __init__(self, content, children):
        self.content = content
        self.children = children


class GeneratorAST:

    def __init__(self):
        self.__root = None
        self.__current_node = None

    def add_node(self, parent: Node, new: Node):
        if new is None:
            return

        if parent is None and self.__root is None:
            self.__root = new
            return

        self.__current_node = parent
        self.__current_node.children.append(new)

    def pre_order(self):
        if self.__current_node is None:
            return
        yield self.__current_node
        for child in self.__current_node.children:
            self.__current_node = child

    def flush(self):
        self.__current_node = self.__root

    @property
    def tree(self):
        return self.__root
