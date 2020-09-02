import os
from typing import Generator, Optional, Set, Tuple, Union

import pytest

from gendiff.factories.factory import (AbstractFactory,
                                       FactoryNested, FactoryPlain)
from gendiff.generator_ast.components import Component, ComponentState
from gendiff.products.abstract_product import AbstractProduct
from gendiff.products.product_config import NestedCONFIG, PlainCONFIG
from gendiff.products.product_json import NestedJSON, PlainJSON
from gendiff.products.product_yaml import NestedYAML, PlainYAML


def get_product(type_: str) -> AbstractProduct:
    """
    Возращает продукт для теста
    :param type_:
    :return:
    """
    if type_ == 'json':
        return NestedJSON()
    elif type_ == 'yaml':
        return NestedYAML()
    elif type_ == 'ini':
        return NestedCONFIG()
    else:
        raise TypeError


@pytest.fixture(scope="function", params=[
    'json',
    'yaml',
    'ini'
])
def setup_compare_test(request) -> Generator:
    project_dir = os.path.dirname(__file__)
    files_dir = os.path.join(project_dir, "test_files/")

    path_file_before = os.path.join(files_dir, "before." + request.param)
    path_file_after = os.path.join(files_dir, "after." + request.param)

    product = get_product(request.param)

    with open(path_file_before, 'r') as file_1, \
            open(path_file_after, 'r') as file_2:
        des_data_1 = product.read(file_1)
        des_data_2 = product.read(file_2)
        yield des_data_1, des_data_2, product


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
    'yaml',
    'ini'
])
def setup_decompot(request) -> Tuple[Union[
                                         NestedJSON,
                                         NestedYAML,
                                         NestedCONFIG], str]:
    if request.param == 'json':
        return NestedJSON(), request.param
    elif request.param == 'yaml':
        return NestedYAML(), request.param
    else:
        return NestedCONFIG(), request.param


@pytest.fixture(scope="function", params=[
    'json',
    'yaml',
    'ini'
])
def setup_is_complex(request) -> Union[PlainJSON,
                                       PlainYAML,
                                       PlainCONFIG]:
    if request.param == 'json':
        return PlainJSON()
    elif request.param == 'yaml':
        return PlainYAML()
    else:
        return PlainCONFIG()


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
    'normal',
    'not equal format',
])
def setup_parse_func(request) -> Generator:
    project_dir = os.path.dirname(__file__)
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
