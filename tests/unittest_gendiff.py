"""
Этот модуль содержит в себе юнит тесты для консольного скрипта gendiff
"""
import pytest

from gendiff.factories.factory import FactoryNested, FactoryPlain
from gendiff.generator_ast.components import Component, ComponentState
from gendiff.parser import (get_concrete_factory,
                            get_concrete_product, read_file, parse)
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
        elif type_test == 'yaml':
            assert '\n    Hello, world: Hello, Python' \
                   == product.decompot({'Hello, world': 'Hello, Python'})
        assert str(52) == product.decompot(52)
        assert str('Hello') == product.decompot('Hello')
        assert str(45, ) == product.decompot(45, )
        assert str({'set'}) == product.decompot({'set'})

    def test_is_complex(self, setup_is_complex):
        product = setup_is_complex
        assert '[complex value]' == product.is_complex({'Hello': 'Hello'})
        assert str(52) == product.is_complex(52)
        assert str('Hello') == product.is_complex('Hello')
        assert str(45, ) == product.is_complex(45, )
        assert str({'set'}) == product.is_complex({'set'})

    @pytest.mark.parametrize("format_", ['json', 'yaml', 'config'])
    def test_func_get_concrete_product(self, format_, setup_get_product):
        factory, type_test = setup_get_product
        product = get_concrete_product(factory, format_)
        if type_test == 'nested':
            if format_ == 'json':
                assert isinstance(product, NestedJSON)
            elif format_ == 'yaml':
                assert isinstance(product, NestedYAML)
            else:
                assert isinstance(product, NestedCONFIG)
        elif type_test == 'plain':
            if format_ == 'json':
                assert isinstance(product, PlainJSON)
            elif format_ == 'yaml':
                assert isinstance(product, PlainYAML)
            else:
                assert isinstance(product, PlainCONFIG)
        else:
            assert product is None

    @pytest.mark.parametrize("type_test", ['nested', 'plain', 'not_if_this'])
    def test_func_get_concrete_factory(self, type_test):
        factory = get_concrete_factory(type_test)
        if type_test == 'nested':
            assert isinstance(factory, FactoryNested)
        elif type_test == 'plain':
            assert isinstance(factory, FactoryPlain)
        else:
            assert factory is None

    @pytest.mark.parametrize("type_test", ['nested', 'plain'])
    @pytest.mark.parametrize("format_", ['json', 'yaml'])
    def test_raise_in_render(self, type_test, format_, setup_render_test):
        invalid_ast = setup_render_test
        if type_test == 'nested':
            if format_ == 'json':
                product = NestedJSON()
                with pytest.raises(TypeError):
                    product.render(invalid_ast)
            elif format_ == 'yaml':
                product = NestedYAML()
                with pytest.raises(TypeError):
                    product.render(invalid_ast)
        elif type_test == 'plain':
            if format_ == 'json':
                product = PlainJSON()
                with pytest.raises(TypeError):
                    product.render(invalid_ast)
            elif format_ == 'yaml':
                product = PlainYAML()
                with pytest.raises(TypeError):
                    product.render(invalid_ast)

    def test_read_file(self, setup_read_file_test):
        invalid_file = setup_read_file_test
        with pytest.raises(TypeError):
            read_file(invalid_file)

    def test_components(self):
        component_1 = Component('param', ComponentState.INSERT, 45)
        component_2 = Component('second param', ComponentState.DELETE, 'deleted')

        assert str(component_1) == 'param, ComponentState.INSERT, 45'
        assert str(component_2) == 'second param, ComponentState.DELETE, deleted'

        assert component_1 == component_1
        assert component_1 != component_2

    @pytest.mark.parametrize("format_", ['nested', 'plain', 'bad'])
    def test_parse(self, format_, setup_parse_func):
        io_1, io_2, param = setup_parse_func
        if param == 'normal':
            if format_ != 'bad':
                assert parse(io_1, io_2, format_) == 'Good'
            else:
                assert parse(io_1, io_2, format_) == 'Internal error'
        else:
            assert parse(io_1, io_2, format_) == 'Not equal format file'
