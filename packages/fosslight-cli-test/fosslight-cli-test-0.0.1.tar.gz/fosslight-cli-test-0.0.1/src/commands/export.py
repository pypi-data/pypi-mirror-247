import datetime

import click

from src.commands.base import cli
from src.services.project import ProjectService
from src.services.self_check import SelfCheckService
from src.utils.json import pretty_print_dict


@cli.group()
def export():
    pass


@export.group("project")
def export_project():
    pass


@export_project.command("bom")
@click.option("--prjId", "prjId", required=True, help="project id")
@click.option("--mergeSaveFlag", "mergeSaveFlag", help="mergeSaveFlag")
def export_project_bom(prjId, mergeSaveFlag):
    response = ProjectService().export_bom(prjId, mergeSaveFlag)
    with open(f"bom_{int(datetime.datetime.now().timestamp())}.xlsx", "wb") as f:
        f.write(response.content)
    print("Success: Export project bom")


@export_project.command("bomJson")
@click.option("--prjId", "prjId", required=True, help="project id")
def export_project_bom_json(prjId):
    data = ProjectService().export_bom_json(prjId)
    pretty_print_dict(data)


@export.command("selfCheck")
@click.option("--selfCheckId", "selfCheckId", required=True, help="selfCheck id")
def export_self_check(selfCheckId):
    response = SelfCheckService().export(selfCheckId)
    with open(f"bom_{int(datetime.datetime.now().timestamp())}.xlsx", "wb") as f:
        f.write(response.content)
    print("Success: Export self-check")
