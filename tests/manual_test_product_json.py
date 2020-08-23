from gendiff.products.product_json import JsonJSON
from gendiff.generator_ast.generator_ast import GeneratorAST


if __name__ == '__main__':
    an = JsonJSON()
    gen_before = GeneratorAST()
    gen_after = GeneratorAST()

    with open('before.json', 'r') as before, open('after.json') as after:
        str_data_before = before.read()
        str_data_after = after.read()

        des_data_before = an.read(str_data_before)
        des_data_after = an.read(str_data_after)

        an.research(des_data_before, None, gen_before)
        an.research(des_data_after, None, gen_after)

        # for i in gen_before.pre_order(gen_before.tree):
        #     print(i)

        an.compare(gen_before, gen_after)
