"""
Этот модуль содержит в себе юнит тесты для консольного скрипта gendiff
"""
import os
import json
import yaml
import pytest

from gendiff.products.product_json import NestedJSON
from gendiff.products.product_yaml import NestedYAML
from gendiff.generator_ast.components import Component, ComponentState


def desereliaze(data: str, type_: str):
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


def read_data_from_file(format_: str, type_: str):
    """
    Безопасное открытие файлов и чтение данных из тестовых фикстур
    :param format_: json, yaml, ini
    :param type_: plain, nested
    :return: tuple with data
    """
    project_dir = os.path.dirname(os.path.dirname(__file__))
    files_dir = os.path.join(project_dir, "test_files/" + format_)

    path_file_before = os.path.join(files_dir, "before." + type_)
    path_file_after = os.path.join(files_dir, "after." + type_)

    with open(path_file_before, 'r') as file_1, open(path_file_after, 'r') as file_2:
        data_1 = file_1.read()
        data_2 = file_2.read()

        des_data_1 = desereliaze(data_1, type_)
        des_data_2 = desereliaze(data_2, type_)
        return des_data_1, des_data_2


reference_ast = {Component('group3', ComponentState.INSERT, {'fee': '100500'}),
                 Component('group2', ComponentState.DELETE, {'abc': '12345'}),
                 Component('group1', ComponentState.CHILDREN, {
                     Component('baz', ComponentState.UPDATE, ('bas', 'bars')),
                     Component('nest', ComponentState.UPDATE, (
                         {'key': 'value'},
                         'str'
                     ))
                 }),
                 Component('common', ComponentState.CHILDREN, {
                     Component('setting2', ComponentState.DELETE, '200'),
                     Component('setting3', ComponentState.UPDATE, (
                         True,
                         {'key': 'value'}
                     )),
                     Component('setting4', ComponentState.INSERT, 'blah blah'),
                     Component('setting5', ComponentState.INSERT, {
                         'key5': 'value5'
                     }),
                     Component('setting6', ComponentState.CHILDREN, {
                         Component('ops', ComponentState.INSERT, 'vops')
                     })
                 })}


def test_case_diff_json():
    """
    Тест кейс для JSON типа
    :return:
    """
    product = NestedJSON()
    ast = product.compare(*read_data_from_file('nested', 'json'))

    assert reference_ast == ast


def test_case_diff_yaml():
    """
    Тест кейс для YAML типа
    :return:
    """
    product = NestedYAML()
    ast = product.compare(*read_data_from_file('nested', 'yaml'))

    assert reference_ast == ast


def test_case_diff_config():
    """
    Тест кейс для INI типа
    :return:
    """
