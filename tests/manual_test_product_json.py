from gendiff.products.product_json import JsonJSON
from gendiff.generator_ast.generator_ast import GeneratorAST


if __name__ == '__main__':
    an = JsonJSON()
    gen = GeneratorAST()
    with open('in.json', 'r') as file:
        str_data = file.read()
        des_data = an.read(str_data)
        an.research(des_data, None, gen)

        for i in gen.pre_order(gen.tree):
            print(i)
