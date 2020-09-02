from gendiff.products.product_config import NestedCONFIG


if __name__ == '__main__':
    n = NestedCONFIG()
    with open('../../tests/test_files/before.ini', 'r') as file:
        print(n.read(file))