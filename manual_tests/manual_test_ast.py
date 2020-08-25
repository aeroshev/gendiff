# from gendiff.generator_ast.generator_ast import GeneratorAST, Node


if __name__ == '__main__':
    gen = GeneratorAST()
    root = gen.add_node(None, Node(1, []))
    node_1 = gen.add_node(root, Node(2, []))
    node_2 = gen.add_node(root, Node(3, []))
    node_1_1 = gen.add_node(node_1, Node(11, []))
    for node in gen.pre_order(root):
        print(node.content)
