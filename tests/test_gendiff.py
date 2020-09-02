"""
Этот модуль содержит в себе юнит тесты для консольного скрипта gendiff
"""
from typing import Set

import pytest

from gendiff.factories.factory import FactoryNested, FactoryPlain
from gendiff.generator_ast.components import Component, ComponentState
from gendiff.parser import get_concrete_factory, get_concrete_product, parse
from gendiff.products.product_config import NestedCONFIG, PlainCONFIG
from gendiff.products.product_json import NestedJSON, PlainJSON
from gendiff.products.product_yaml import NestedYAML, PlainYAML


class TestGendiff:
    reference_ast: Set[Component] = \
        {Component('group3',
                   ComponentState.INSERT,
                   {'fee': '100500'}),
         Component('group2',
                   ComponentState.DELETE,
                   {'abc': '12345'}),
         Component('group1',
                   ComponentState.CHILDREN, {
                       Component('baz',
                                 ComponentState.UPDATE,
                                 ('bas', 'bars')),
                       Component('nest',
                                 ComponentState.UPDATE, (
                                     {'key': 'value'},
                                     'str'
                                 ))
                   }),
         Component('common', ComponentState.CHILDREN, {
             Component('setting2',
                       ComponentState.DELETE,
                       '200'),
             Component('setting3',
                       ComponentState.UPDATE, (
                           True,
                           {'key': 'value'}
                       )),
             Component('setting4',
                       ComponentState.INSERT,
                       'blah blah'),
             Component('setting5',
                       ComponentState.INSERT, {
                           'key5': 'value5'
                       }),
             Component('setting6',
                       ComponentState.CHILDREN, {
                           Component('ops',
                                     ComponentState.INSERT,
                                     'vops')
                       })
         })}

    reference_ast_ini: Set[Component] = \
        {Component('common',
                   ComponentState.CHILDREN,
                   {Component('setting2',
                              ComponentState.DELETE,
                              '200'),
                    Component('setting3',
                              ComponentState.DELETE,
                              'true'
                              )}
                   ),
         Component('common.setting3',
                   ComponentState.INSERT,
                   {'key': 'value'}
                   ),
         Component('common.setting4',
                   ComponentState.INSERT,
                   {'setting4': 'blah blah'}
                   ),
         Component('common.setting5',
                   ComponentState.INSERT,
                   {'key5': 'value5'}
                   ),
         Component('common.setting6',
                   ComponentState.CHILDREN,
                   {
                       Component('ops',
                                 ComponentState.INSERT,
                                 'vops')
                   }
                   ),
         Component('group1',
                   ComponentState.CHILDREN,
                   {Component('nest',
                              ComponentState.INSERT,
                              'str'),
                    Component('baz',
                              ComponentState.UPDATE,
                              ('bas', 'bars')
                              )
                    }),
         Component('group1.nest',
                   ComponentState.DELETE,
                   {'key': 'value'}),
         Component('group2',
                   ComponentState.DELETE,
                   {'abc': '12345'})
         }

    def test_compare_func(self, setup_compare_test) -> None:
        des_data_before, des_data_after, product = setup_compare_test
        diff = product.compare(des_data_before, des_data_after)
        if isinstance(product, NestedCONFIG):
            assert diff == self.reference_ast_ini
        else:
            assert diff == self.reference_ast

    def test_decompot(self, setup_decompot) -> None:
        product, type_test = setup_decompot
        if type_test == 'json':
            assert '{\n Hello, world: Hello, Python\n}' \
                   == product.decomposition({'Hello, world': 'Hello, Python'})
        elif type_test == 'yaml':
            assert '\n    Hello, world: Hello, Python' \
                   == product.decomposition({'Hello, world': 'Hello, Python'})
        elif type_test == 'ini':
            assert 'Hello, world=Hello, Python' \
                   == product.decomposition({'Hello, world': 'Hello, Python'})

        assert str(52) == product.decomposition(52)
        assert str('Hello') == product.decomposition('Hello')
        assert str(45, ) == product.decomposition(45, )
        assert str({'set'}) == product.decomposition({'set'})

    def test_is_complex(self, setup_is_complex) -> None:
        product = setup_is_complex
        assert '[complex value]' == product.is_complex({'Hello': 'Hello'})
        assert str(52) == product.is_complex(52)
        assert str('Hello') == product.is_complex('Hello')
        assert str(45, ) == product.is_complex(45, )
        assert str({'set'}) == product.is_complex({'set'})

    @pytest.mark.parametrize("format_", ['json', 'yaml', 'ini'])
    def test_func_get_concrete_product(self, format_, setup_get_product) -> None:
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

    @pytest.mark.parametrize("format_", ['json', 'yaml', 'ini'])
    def test_func_get_concrete_product_exception(self, format_: str) -> None:
        with pytest.raises(SystemError):
            get_concrete_product(None, format_)

    @pytest.mark.parametrize("type_test", ['nested', 'plain'])
    def test_func_get_concrete_factory(self, type_test) -> None:
        factory = get_concrete_factory(type_test)
        if type_test == 'nested':
            assert isinstance(factory, FactoryNested)
        elif type_test == 'plain':
            assert isinstance(factory, FactoryPlain)

    def test_func_get_concrete_factory_exception(self) -> None:
        with pytest.raises(SystemError):
            get_concrete_factory('wrong_format')

    @pytest.mark.parametrize("type_test", ['nested', 'plain'])
    @pytest.mark.parametrize("format_", ['json', 'yaml', 'ini'])
    def test_raise_in_render(self, type_test: str, format_: str, setup_render_test) -> None:
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

    def test_components(self) -> None:
        component_1 = Component('param',
                                ComponentState.INSERT,
                                45)
        component_2 = Component('second param',
                                ComponentState.DELETE,
                                'deleted')

        assert str(component_1) == 'param, ComponentState.INSERT, 45'
        assert str(component_2) == 'second param, ' \
                                   'ComponentState.DELETE, deleted'

        assert component_1 == component_1
        assert component_1 != component_2

    @pytest.mark.parametrize("format_", ['nested', 'plain', 'bad'])
    def test_parse(self, format_: str, setup_parse_func) -> None:
        io_1, io_2, param = setup_parse_func
        if param == 'normal':
            if format_ != 'bad':
                assert parse(io_1, io_2, format_) == 'Good'
            else:
                assert parse(io_1, io_2, format_) == 'Invalid format report'
        elif param == 'bad extension':
            if format_ != 'bad':
                assert parse(io_1, io_2, format_) == 'Not support file extension'
            else:
                assert parse(io_1, io_2, format_) == 'Invalid format report'
        else:
            assert parse(io_1, io_2, format_) == 'Not equal format file'
