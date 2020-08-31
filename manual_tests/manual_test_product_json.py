from gendiff.products.product_json import NestedJSON, PlainJSON
import os


if __name__ == '__main__':
    an = NestedJSON()
    p = PlainJSON()

    project_dir = os.path.dirname(os.path.dirname(__file__))
    files_dir = os.path.join(project_dir, "test_files")

    path_file_before = os.path.join(files_dir, "before.json")
    path_file_after = os.path.join(files_dir, "after.json")

    with open(path_file_before, 'r') as before, open(path_file_after, 'r') as after:
        str_data_before = before.read()
        str_data_after = after.read()

        des_data_before = an.read(str_data_before)
        des_data_after = an.read(str_data_after)

        diff = an.compare(des_data_before, des_data_after)

        an.render(diff)
        p.render(diff)
