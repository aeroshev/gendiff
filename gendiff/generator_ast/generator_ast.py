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
            return self.__root

        self.__current_node = parent
        self.__current_node.children.append(new)

        return self.__current_node.children[-1]

    def pre_order(self, node):
        if node is None:
            return
        yield node
        for child in node.children:
            for x in self.pre_order(child):
                yield x

    def flush(self):
        self.__current_node = self.__root

    @property
    def tree(self):
        return self.__root
