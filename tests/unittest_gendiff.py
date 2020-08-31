"""
Этот модуль содержит в себе юнит тесты для консольного скрипта gendiff
"""

from gendiff.generator_ast.components import Component, ComponentState
from gendiff.parser import get_concrete_factory, get_concrete_product
from gendiff.products.product_config import NestedCONFIG, PlainCONFIG
from gendiff.products.product_json import NestedJSON, PlainJSON
from gendiff.products.product_yaml import NestedYAML, PlainYAML


class TestGendiff:
    reference_ast = {Component('group3',
                               ComponentState.INSERT,
                               {'fee': '100500'}),
                     Component('group2',
                               ComponentState.DELETE,
                               {'abc': '12345'}),
                     Component('group1', ComponentState.CHILDREN, {
                         Component('baz',
                                   ComponentState.UPDATE,
                                   ('bas', 'bars')),
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
                         Component('setting4',
                                   ComponentState.INSERT,
                                   'blah blah'),
                         Component('setting5', ComponentState.INSERT, {
                             'key5': 'value5'
                         }),
                         Component('setting6', ComponentState.CHILDREN, {
                             Component('ops', ComponentState.INSERT, 'vops')
                         })
                     })}

    def test_compare_func(self, setup_compare_test):
        des_data_before, des_data_after, product = setup_compare_test
        diff = product.compare(des_data_before, des_data_after)
        assert diff == self.reference_ast

    def test_decompot(self, setup_decompot):
        product, type_test = setup_decompot
        if type_test == 'json':
            assert '{\n Hello, world: Hello, Python\n}' \
                   == product.decompot({'Hello, world': 'Hello, Python'})
        else:
            assert '\n    Hello, world: Hello, Python' \
                   == product.decompot({'Hello, world': 'Hello, Python'})
        assert str(52) == product.decompot(52)
        assert str('Hello') == product.decompot('Hello')
        assert str(45,) == product.decompot(45,)
        assert str({'set'}) == product.decompot({'set'})

    def test_is_complex(self, setup_is_complex):
        product = setup_is_complex
        assert '[complex value]' == product.is_complex({'Hello': 'Hello'})
        assert str(52) == product.is_complex(52)
        assert str('Hello') == product.is_complex('Hello')
        assert str(45,) == product.is_complex(45,)
        assert str({'set'}) == product.is_complex({'set'})

    def test_func_get_concrete_product(self, setup_get_product):
        factory, type_test = setup_get_product
        if type_test == 'nested':
            product_json = get_concrete_product(factory, 'json')
            product_yaml = get_concrete_product(factory, 'yaml')
            product_config = get_concrete_product(factory, 'config')
            assert isinstance(product_json, NestedJSON)
            assert isinstance(product_yaml, NestedYAML)
            assert isinstance(product_config, NestedCONFIG)
        elif type_test == 'plain':
            product_json = get_concrete_product(factory, 'json')
            product_yaml = get_concrete_product(factory, 'yaml')
            product_config = get_concrete_product(factory, 'config')
            assert isinstance(product_json, PlainJSON)
            assert isinstance(product_yaml, PlainYAML)
            assert isinstance(product_config, PlainCONFIG)
        else:
            product_json = get_concrete_product(factory, 'json')
            product_yaml = get_concrete_product(factory, 'yaml')
            product_config = get_concrete_product(factory, 'config')
            assert product_json is None
            assert product_yaml is None
            assert product_config is None
