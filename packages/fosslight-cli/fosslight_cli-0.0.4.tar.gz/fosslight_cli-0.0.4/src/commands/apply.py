import click

from src.apply.create_project import create_project
from src.commands.base import cli
from src.enums.apply import Kind
from src.utils.output import set_output_result
from src.utils.yaml import read_yaml


@cli.group("apply")
def apply():
    pass


@apply.command("yaml")
@click.option('--file', '-f', 'file', required=True, help="yaml file path")
def apply_yaml(file):
    data = read_yaml(file)
    kind = data['kind']
    assert kind in Kind.choices, f"invalid kind - available kinds: {', '.join(Kind.choices)}"

    if kind == Kind.CREATE_PROJECT:
        prjId = create_project(data)
        set_output_result(prjId)
