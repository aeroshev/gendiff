"""
Этот модуль содержит в себе юнит тесты для консольного скрипта gendiff
"""


from gendiff.generator_ast.components import Component, ComponentState


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


def test_compare_func(setup_compare_test):
    des_data_before, des_data_after, product = setup_compare_test
    diff = product.compare(des_data_before, des_data_after)
    assert diff == reference_ast
