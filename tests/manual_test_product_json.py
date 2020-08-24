from gendiff.products.product_json import JsonJSON
from gendiff.generator_ast.components import Composite, Root, WalkerTree


if __name__ == '__main__':
    an = JsonJSON()

    with open('before.json', 'r') as before, open('after.json') as after:
        str_data_before = before.read()
        str_data_after = after.read()

        des_data_before = an.read(str_data_before)
        des_data_after = an.read(str_data_after)

        print(des_data_before)

        # diff = an.compare(des_data_before, des_data_after)
        # an.render(diff)

