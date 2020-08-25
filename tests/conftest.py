import pytest
import os
import json


def desereliaze(data, type_: str):
    res = None
    if type_ == 'json':
        res = json.loads(data)
    elif type_ == 'yaml':
        pass
    return res


# @pytest.fixture(scope='function', autouse=True)
def read_data_from_file(param: tuple):
    project_dir = os.path.dirname(os.path.dirname(__file__))
    files_dir = os.path.join(project_dir, "test_files/" + param[0])

    path_file_before = os.path.join(files_dir, "before." + param[1])
    path_file_after = os.path.join(files_dir, "after." + param[1])

    with open(path_file_before, 'r') as file_1, open(path_file_after, 'r') as file_2:
        data_1 = file_1.read()
        data_2 = file_2.read()

        des_data_1 = desereliaze(data_1, param[1])
        des_data_2 = desereliaze(data_2, param[1])
        yield des_data_1, des_data_2
