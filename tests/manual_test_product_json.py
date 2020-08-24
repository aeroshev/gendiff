from gendiff.products.product_json import JsonJSON


if __name__ == '__main__':
    an = JsonJSON()

    with open('before.json', 'r') as before, open('after.json') as after:
        str_data_before = before.read()
        str_data_after = after.read()

        des_data_before = an.read(str_data_before)
        des_data_after = an.read(str_data_after)

        diff = an.compare(des_data_before, des_data_after)
        for i in diff:
            print(i.param)
            print(i.state)
            print(i.value)
            print(' '*100)
        # an.render(diff)

