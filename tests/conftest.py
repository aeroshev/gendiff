import pytest
import os
import json
import yaml

from typing import Tuple, Optional

from gendiff.products.abstract_product import AbstractProduct
from gendiff.products.product_json import NestedJSON
from gendiff.products.product_yaml import NestedYAML


def deserialization(data: str, type_: str):
    """
    Десериализация файловых данных в python тип
    :param data:
    :param type_:
    :return:
    """
    res = None
    if type_ == 'json':
        res = json.loads(data)
    elif type_ == 'yaml':
        res = yaml.load(data, yaml.Loader)
    elif type_ == 'ini':
        pass
    return res


def get_product(type_: str) -> Optional[AbstractProduct]:
    """
    Возращает продукт для теста
    :param type_:
    :return:
    """
    product = None
    if type_ == 'json':
        product = NestedJSON()
    elif type_ == 'yaml':
        product = NestedYAML()
    elif type_ == 'ini':
        pass
    return product


@pytest.fixture(scope="function", params=[
    'json',
    'yaml'
])
def setup_compare_test(request) -> Tuple[dict, dict, AbstractProduct]:
    project_dir = os.path.dirname(os.path.dirname(__file__))
    files_dir = os.path.join(project_dir, "test_files/")

    path_file_before = os.path.join(files_dir, "before." + request.param)
    path_file_after = os.path.join(files_dir, "after." + request.param)

    product = get_product(request.param)

    with open(path_file_before, 'r') as file_1, open(path_file_after, 'r') as file_2:
        data_1 = file_1.read()
        data_2 = file_2.read()

        des_data_1 = deserialization(data_1, request.param)
        des_data_2 = deserialization(data_2, request.param)
        return des_data_1, des_data_2, product
