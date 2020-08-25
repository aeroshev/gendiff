from gendiff.products.product_yaml import JsonYAML


if __name__ == '__main__':
    y = JsonYAML()

    with open('before.yaml', 'r') as file_1, open('after.yaml', 'r') as file_2:
        s_1 = file_1.read()
        s_2 = file_2.read()

        des_1 = y.read(s_1)
        des_2 = y.read(s_2)

        diff = y.compare(des_1, des_2)
        print(diff)
        y.render(diff)
