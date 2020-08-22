from gendiff.products.product_json import JsonJSON


if __name__ == '__main__':
    an = JsonJSON()
    with open('in.json', 'r') as file:
        str_data = file.read()
        des_data = an.read(str_data)
        for node in an.research(des_data):
            print(node)
