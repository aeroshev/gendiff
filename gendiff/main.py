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


# TODO Maybe I need global abstract product
def get_concrete_product(factory: AbstractFactory):
    pass


def get_type_file(file_1) -> str:
    pass


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
@click.argument('firstConfig', type=click.File('r'))
@click.argument('secondConfig', type=click.File('r'))
def cli(format, firstConfig, secondConfig):
    """
    Compares two configuration files and shows a difference.
    """
    click.echo('Hello, world!')
