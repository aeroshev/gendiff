import click
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
    if format_ == 'json':
        product = factory.create_json()
    elif format_ == 'plain':
        product = factory.create_plain()
    return product


def read_file(file_name) -> str:
    info = file_name.read()
    return info


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# TODO find file this number version (in setup.py)
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', required=False, is_flag=True, callback=print_version, expose_value=False,
              is_eager=True, help='output the version program')
@click.option('-f', '--format', required=False, default='json', help='output format')
@click.argument('first_config', type=click.File('r'))
@click.argument('second_config', type=click.File('r'))
def cli(format, first_config, second_config):
    """
    Compares two configuration files and shows a difference.
    """
    click.echo(first_config.name.split('.')[-1])
    click.echo('Hello, world!')
    click.echo(read_file(first_config))
