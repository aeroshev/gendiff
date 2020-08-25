from gendiff.products.product_yaml import NestedYAML, PlainYAML
import os


if __name__ == '__main__':
    y = NestedYAML()
    py = PlainYAML()

    project_dir = os.path.dirname(os.path.dirname(__file__))
    files_dir = os.path.join(project_dir, "test_files/nested")

    path_file_before = os.path.join(files_dir, "before.yaml")
    path_file_after = os.path.join(files_dir, "after.yaml")

    with open(path_file_before, 'r') as file_1, open(path_file_after, 'r') as file_2:
        s_1 = file_1.read()
        s_2 = file_2.read()

        des_1 = y.read(s_1)
        des_2 = y.read(s_2)

        diff = y.compare(des_1, des_2)

        y.render(diff)
        py.render(diff)
