from gendiff.products.product_config import NestedCONFIG, PlainCONFIG


if __name__ == '__main__':
    n = PlainCONFIG()
    with open('../../tests/test_files/before.ini', 'r') as file_1, \
            open('../../tests/test_files/after.ini', 'r') as file_2:
        res_1 = n.read(file_1)
        res_2 = n.read(file_2)
        diff = n.compare(res_1, res_2)
        n.render(diff)
