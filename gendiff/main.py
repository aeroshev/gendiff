import click
import gendiff as gf


# TODO find file this number version (in setup.py)
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()


@click.command()
@click.option('-v', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option('-f', '--format', required=False, default='json')
def cli(version, format):
    click.echo('Hello, world!')
