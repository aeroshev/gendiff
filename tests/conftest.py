import json
import os
from typing import Generator, Optional, Set, Tuple, Union

import pytest
import yaml

from gendiff.factories.factory import (AbstractFactory,
                                       FactoryNested, FactoryPlain)
from gendiff.generator_ast.components import Component, ComponentState
from gendiff.products.abstract_product import AbstractProduct
from gendiff.products.product_json import NestedJSON, PlainJSON
from gendiff.products.product_yaml import NestedYAML, PlainYAML


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

    with open(path_file_before, 'r') as file_1, \
            open(path_file_after, 'r') as file_2:
        data_1 = file_1.read()
        data_2 = file_2.read()

        des_data_1 = deserialization(data_1, request.param)
        des_data_2 = deserialization(data_2, request.param)
        return des_data_1, des_data_2, product


@pytest.fixture(scope="function", params=[
    'nested',
    'plain',
    'not_of_this'
])
def setup_get_product(request) -> Tuple[Optional[AbstractFactory], str]:
    if request.param == 'nested':
        return FactoryNested(), request.param
    elif request.param == 'plain':
        return FactoryPlain(), request.param
    else:
        return None, request.param


@pytest.fixture(scope="function", params=[
    'json',
    'yaml'
])
def setup_decompot(request) -> Tuple[Union[NestedJSON, NestedYAML], str]:
    if request.param == 'json':
        return NestedJSON(), request.param
    else:
        return NestedYAML(), request.param


@pytest.fixture(scope="function", params=[
    'json',
    'yaml'
])
def setup_is_complex(request) -> Union[PlainJSON, PlainYAML]:
    if request.param == 'json':
        return PlainJSON()
    else:
        return PlainYAML()


@pytest.fixture(scope="function", params=[
    'try invalid tuple',
    'try invalid set',
    'try invalid state'
])
def setup_render_test(request) -> Set[Component]:
    invalid_tuple_ast: Set[Component] = {Component('insert',
                                                   ComponentState.INSERT,
                                                   'new_value'),
                                         Component('invalid_update',
                                                   ComponentState.UPDATE,
                                                   'not_a_tuple'),
                                         Component('delete',
                                                   ComponentState.DELETE,
                                                   45)}
    invalid_set_ast: Set[Component] = {Component('insert',
                                                 ComponentState.INSERT,
                                                 'new_value'),
                                       Component('invalid children',
                                                 ComponentState.CHILDREN,
                                                 'not_a_set'),
                                       Component('delete',
                                                 ComponentState.DELETE,
                                                 45)}
    invalid_state_ast: Set[Component] = {Component('insert',
                                                   ComponentState.INSERT,
                                                   'new_value'),
                                         Component('invalid_state',
                                                   -1,
                                                   'invalid_state'),
                                         Component('delete',
                                                   ComponentState.DELETE,
                                                   45)}
    if request.param == 'try invalid tuple':
        return invalid_tuple_ast
    elif request.param == 'try invalid set':
        return invalid_set_ast
    else:
        return invalid_state_ast


@pytest.fixture(scope="function", params=[
    'string',
    'number',
    'structure'
])
def setup_read_file_test(request):
    if request.param == 'string':
        return 'not_a_file'
    elif request.param == 'number':
        return 42
    else:
        return {'Hello': 'World!'}


@pytest.fixture(scope="function", params=[
    'normal',
    'not equal format',
])
def setup_parse_func(request) -> Generator:
    project_dir = os.path.dirname(os.path.dirname(__file__))
    files_dir = os.path.join(project_dir, "test_files/")

    path_file_before = os.path.join(files_dir, "before.json")
    path_file_after = os.path.join(files_dir, "after.json")
    path_file_after_yaml = os.path.join(files_dir, "after.yaml")

    if request.param == 'normal':
        with open(path_file_before, 'r') as file_1, \
                open(path_file_after, 'r') as file_2:
            yield file_1, file_2, str(request.param)
    else:
        with open(path_file_before, 'r') as file_1, \
                open(path_file_after_yaml, 'r') as file_2:
            yield file_1, file_2, str(request.param)
