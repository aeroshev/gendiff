# class Node:
#     __slots__ = ['content', 'children']
#
#     def __init__(self, content, children):
#         self.content = content
#         self.children = children
#
#     def __str__(self):
#         return self.content
from gendiff.generator_ast.components import Component, Composite, Leaf


# class GeneratorAST:
#     __slots__ = ['__root']
#
#     def __init__(self):
#         self.__root = None
#
#     def add_node(self, component: Component):
#         if component is None:
#             raise KeyError
#         component.add(component)
#
#     def pre_order(self, node):
#         if node is None:
#             return
#         yield node
#         for child in node.children:
#             for x in self.pre_order(child):
#                 yield x
#
#     @property
#     def tree(self):
#         return self.__root
