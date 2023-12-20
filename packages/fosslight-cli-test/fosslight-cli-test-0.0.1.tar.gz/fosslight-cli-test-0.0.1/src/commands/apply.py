import click
import yaml

from src.apply.create_project import create_project
from src.commands.base import cli
from src.enums.apply import Kind
from src.utils.yaml import read_yaml


@cli.command("apply")
@click.option('--file', '-f', 'file', required=True, help="yaml file path")
def apply(file):
    data = read_yaml(file)
    kind = data['kind']
    assert kind in Kind.choices, f"invalid kind - available kinds: {', '.join(Kind.choices)}"

    if kind == Kind.CREATE_PROJECT:
        create_project(data)
