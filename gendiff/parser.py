from gendiff.factories.factory import FactoryNested, FactoryPlain, AbstractFactory


def get_concrete_product(factory: AbstractFactory, file_type: str):
    product = None
    if file_type == 'json':
        product = factory.create_json()
    elif file_type == 'yaml':
        product = factory.create_yaml()
    elif file_type == 'config':
        product = factory.create_config()
    return product


def get_concrete_factory(format_: str) -> AbstractFactory:
    factory = None
    if format_ == 'nested':
        factory = FactoryNested()
    elif format_ == 'plain':
        factory = FactoryPlain()
    return factory


def read_file(file_name) -> str:
    return file_name.read()


def parse(first_config, second_config, format_):
    f_format_file = first_config.name.split('.')[-1]
    s_format_file = second_config.name.split('.')[-1]

    if f_format_file == s_format_file:
        factory = get_concrete_factory(format_)
        product = get_concrete_product(factory, f_format_file)

        first_data = read_file(first_config)
        second_data = read_file(second_config)

        desirealize_1 = product.read(first_data)
        desirealize_2 = product.read(second_data)

        diff = product.compare(desirealize_1, desirealize_2)
        product.render(diff)

        return 'Good'
    else:
        return 'Not equal format file'
