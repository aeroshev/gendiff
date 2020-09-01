"""
Этот модуль содержит функции которые занимаются обработкой входных параметров и
выбором продукта для обработки файлов
"""
from io import TextIOWrapper
from typing import Optional

from gendiff.factories.factory import (AbstractFactory,
                                       FactoryNested, FactoryPlain)
from gendiff.products.abstract_product import AbstractProduct


def get_concrete_product(factory: AbstractFactory,
                         file_type: str) -> Optional[AbstractProduct]:
    """
    За счёт полученного расширения файла определяет какой конкретный продукт
    необходимо получить
    :param factory: Nested* or Plain* фабрика
    :param file_type: расширение файла
    :return: product (*JSON, *YAML, *CONFIG)
    """
    product = None
    if factory:
        if file_type == 'json':
            product = factory.create_json()
        elif file_type == 'yaml':
            product = factory.create_yaml()
        elif file_type == 'config':
            product = factory.create_config()
    return product


def get_concrete_factory(format_: str) -> Optional[AbstractFactory]:
    """
    По полученному формата возращает фабрику из семейсива Nested или Plain
    :param format_: nested - default or plain
    :return: factory (Nested or Plain)
    """
    factory = None
    if format_ == 'nested':
        factory = FactoryNested()
    elif format_ == 'plain':
        factory = FactoryPlain()
    return factory


def read_file(file_name: TextIOWrapper) -> str:
    """
    Чтение файла.
    Контекстный оператор не используется, т.к. click сам открывает файл
    :param file_name:
    :return: data from file
    """
    if isinstance(file_name, TextIOWrapper):
        return file_name.read()
    else:
        raise TypeError


def parse(first_config: TextIOWrapper,
          second_config: TextIOWrapper,
          format_: str) -> str:
    """
    Происходит основная частьсв работы.
    Содержит в себе вызовы функций чтения из файла, десериализации, сравнения
    и рендера результата сравнения
    :param first_config: file name
    :param second_config: file name
    :param format_: type printing
    :return: status
    """
    f_format_file = first_config.name.split('.')[-1]
    s_format_file = second_config.name.split('.')[-1]

    status = 'Good'

    if f_format_file == s_format_file:
        factory = get_concrete_factory(format_)
        product = get_concrete_product(factory, f_format_file)

        try:
            first_data = read_file(first_config)
            second_data = read_file(second_config)
        except TypeError:
            status = 'Error parse'
            return status

        if product:
            deserialized_1 = product.read(first_data)
            deserialized_2 = product.read(second_data)

            diff = product.compare(deserialized_1, deserialized_2)
            try:
                product.render(diff)
            except TypeError:
                status = 'Render was stopped with error'
        else:
            status = 'Internal error'
    else:
        status = 'Not equal format file'
    return status
