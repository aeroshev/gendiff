import click
from gendiff.parser import parse


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
@click.option('-f', '--format', required=False, default='nested', help='output format')
@click.argument('first_config', type=click.File('r'))
@click.argument('second_config', type=click.File('r'))
def cli(format, first_config, second_config):
    """
    Compares two configuration files and shows a difference.
    """
    res = parse(first_config, second_config, format)
    click.echo(res)
