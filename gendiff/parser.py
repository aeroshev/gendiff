from gendiff.factories.factory import FactoryJSON, FactoryYAML, FactoryCONFIG, AbstractFactory


def get_concrete_factory(file_type: str) -> AbstractFactory:
    factory = None
    if file_type == 'json':
        factory = FactoryJSON()
    elif file_type == 'yaml':
        factory = FactoryYAML()
    elif file_type == 'config':
        factory = FactoryCONFIG()
    return factory


def get_concrete_product(factory: AbstractFactory, format_: str):
    product = None
    if format_ == 'nested':
        product = factory.create_nested()
    elif format_ == 'plain':
        product = factory.create_plain()
    return product


def read_file(file_name) -> str:
    return file_name.read()


def parse(first_config, second_config, format_):
    f_format_file = first_config.name.split('.')[-1]
    s_format_file = second_config.name.split('.')[-1]

    if f_format_file == s_format_file:
        factory = get_concrete_factory(f_format_file)
        product = get_concrete_product(factory, format_)

        first_data = read_file(first_config)
        second_data = read_file(second_config)

        desirealize_1 = product.read(first_data)
        desirealize_2 = product.read(second_data)

        diff = product.compare(desirealize_1, desirealize_2)
        product.render(diff)

        return 'Good'
    else:
        return 'Not equal format file'
