import pytest

from gendiff.generator_ast.generator_ast import GeneratorAST, Node


class TestGeneratorAST:

    def test_tree_ast(self):
        gen = GeneratorAST()
        nodes_list = [Node(1, []), Node(2, []), Node(3, []), Node(4, []), Node(5, []), Node(6, []), Node(7, []),
                      Node(8, []), Node(9, []), Node(10, []), Node(11, []), Node(12, [])]

        parent_root = gen.add_node(None, nodes_list[0])
        parent_1 = gen.add_node(parent_root, nodes_list[1])
        parent_2 = gen.add_node(parent_root, nodes_list[2])
        parent_3 = gen.add_node(parent_root, nodes_list[3])

        parent_1_1 = gen.add_node(parent_1, nodes_list[4])
        parent_1_2 = gen.add_node(parent_1, nodes_list[5])
        parent_1_3 = gen.add_node(parent_1, nodes_list[6])

        parent_2_1 = gen.add_node(parent_2, nodes_list[7])
        parent_2_2 = gen.add_node(parent_2, nodes_list[8])

        parent_1_1_1 = gen.add_node(parent_1_1, nodes_list[9])
        parent_1_3_1 = gen.add_node(parent_1_3, nodes_list[10])
        parent_1_3_2 = gen.add_node(parent_1_3, nodes_list[11])

        root_ = gen.tree

        test_case = [1, 2, 5, 10, 6, 7, 11, 12, 3, 8, 9, 4]

        for test_, node in zip(test_case, gen.pre_order(root_)):
            assert test_ == node.content
            print(f'Test -> {test_}, real -> {node.content}')


if __name__ == '__main__':
    test = TestGeneratorAST()
    test.test_add_node_function()

