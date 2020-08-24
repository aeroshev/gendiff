from gendiff.products.product_yaml import JsonYAML


if __name__ == '__main__':
    y = JsonYAML()

    with open('before.yaml', 'r') as file:
        s = file.read()
        print(y.read(s))
