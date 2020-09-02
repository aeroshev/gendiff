"""
Этот модуль содержит функции которые занимаются обработкой входных параметров и
выбором продукта для обработки файлов
"""
from io import TextIOWrapper
from typing import Optional

from gendiff.factories.factory import (AbstractFactory,
                                       FactoryNested, FactoryPlain)
from gendiff.products.abstract_product import AbstractProduct


def get_concrete_product(factory: Optional[AbstractFactory],
                         file_type: str) -> AbstractProduct:
    """
    За счёт полученного расширения файла определяет какой конкретный продукт
    необходимо получить
    :param factory: Nested* or Plain* фабрика
    :param file_type: расширение файла
    :return: product (*JSON, *YAML, *CONFIG)
    """
    if factory:
        if file_type == 'json':
            return factory.create_json()
        elif file_type == 'yaml':
            return factory.create_yaml()
        elif file_type == 'ini':
            return factory.create_config()
    raise SystemError


def get_concrete_factory(format_: str) -> AbstractFactory:
    """
    По полученному формата возращает фабрику из семейсива Nested или Plain
    :param format_: nested - default or plain
    :return: factory (Nested or Plain)
    """
    if format_ == 'nested':
        return FactoryNested()
    elif format_ == 'plain':
        return FactoryPlain()
    else:
        raise SystemError


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
        # Try get valid factory
        try:
            factory = get_concrete_factory(format_)
        except SystemError:
            status = 'Invalid format report'
            return status
        # Try get valid product
        try:
            product = get_concrete_product(factory, f_format_file)
        except SystemError:
            status = 'Not support file extension'
            return status
        # Try deserialized from file
        try:
            deserialized_1 = product.read(first_config)
            deserialized_2 = product.read(second_config)
        except SystemError:
            status = 'Parse error'
            return status
        # Compare two files
        diff = product.compare(deserialized_1, deserialized_2)
        # Try render report
        try:
            product.render(diff)
        except TypeError:
            status = 'Render was stopped with error'
    else:
        status = 'Not equal format file'
    return status
