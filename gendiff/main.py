"""
Этот модуль является точкой входа в консольный скрипт gendiff
"""
from io import TextIOWrapper
from typing import Any, Sequence, Union

import click
import pkg_resources

from gendiff.parser import parse

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def print_version(ctx: click.Context,
                  param: Union[click.Option, click.Parameter],
                  value:  Sequence[Union[int, bool, str]]) -> Any:
    """
    Узнаёт версию программы просматривая файл setup.py
    :param ctx:
    :param param:
    :param value:
    :return: nothing
    """
    if not value or ctx.resilient_parsing:
        return
    version = pkg_resources.require("gendiff")[0].version
    click.echo('Version ' + version)
    ctx.exit()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', required=False, is_flag=True,
              callback=print_version,
              expose_value=False, is_eager=True,
              help='output the version program')
@click.option('-f', '--format', required=False,
              default='nested', help='output format')
@click.argument('first_config', type=click.File('r'))
@click.argument('second_config', type=click.File('r'))
def cli(format: str, first_config: TextIOWrapper, second_config: TextIOWrapper):
    """
    Compares two configuration files and shows a difference.
    """
    res = 'Error parse'
    try:
        res = parse(first_config, second_config, format)
    except TypeError:
        pass

    click.echo(res)
