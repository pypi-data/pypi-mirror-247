import click

from src.client import get_api_client
from src.commands.base import cli
from src.services.project import ProjectService
from src.services.self_check import SelfCheckService
from src.utils.response import check_response


@cli.group()
def update():
    pass


@update.group("project")
def update_project():
    pass


@update.group("selfCheck")
def update_self_check():
    pass


@update.group("partners")
def update_partners():
    pass


@update_project.command('watchers')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--emailList', 'emailList', required=True, help="watcher emailList")
def update_project_watchers(prjId, emailList):
    ProjectService().update_watchers(prjId, emailList)
    print("success")


@update_project.command('models')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--modelListToUpdate', 'modelListToUpdate', required=True)
def update_project_models(prjId, modelListToUpdate):
    ProjectService().update_model_file(prjId, modelListToUpdate)
    print("Success: Update project model")


@update_project.command('modelFile')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--modelReport', 'modelReport', required=True)
def update_project_model_file(prjId, modelReport):
    ProjectService().update_model_file(prjId, modelReport)
    print("Success: Update project model file")


@update_project.command('scan')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--dir', 'dir', required=True, help="project directory path")
def update_project_scan(prjId, dir):
    ProjectService().scan(prjId, dir)
    print("Success: scan project")


@update_project.command('bin')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--ossReport', 'ossReport')
@click.option('--binaryTxt', 'binaryTxt')
@click.option('--comment', 'comment')
@click.option('--resetFlag', 'resetFlag')
def update_project_bin(
    prjId,
    ossReport,
    binaryTxt,
    comment,
    resetFlag,
):
    ProjectService().update_bin(prjId, ossReport, binaryTxt, comment, resetFlag)
    print("Success: Upload project bin")


@update_project.command('src')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--ossReport', 'ossReport')
@click.option('--comment', 'comment')
@click.option('--resetFlag', 'resetFlag')
def update_project_src(
    prjId,
    ossReport,
    comment,
    resetFlag,
):
    ProjectService().update_src(prjId, ossReport, comment, resetFlag)
    print("Success: Upload project src")


@update_project.command('packages')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--packageFile', 'packageFile', required=True)
@click.option('--verifyFlag', 'verifyFlag')
def update_project_packages(prjId, packageFile, verifyFlag):
    ProjectService().update_packages(prjId, packageFile, verifyFlag)
    print("Success: Upload project packages")


@update_self_check.command('report')
@click.option('--selfCheckId', 'selfCheckId', required=True, help="selfCheck id")
@click.option('--ossReport', 'ossReport')
@click.option('--resetFlag', 'resetFlag')
def update_self_check_report(selfCheckId, ossReport, resetFlag):
    SelfCheckService().update_report(selfCheckId, ossReport, resetFlag)
    print("Success: Upload self-check report")


@update_self_check.command('watchers')
@click.option('--selfCheckId', 'selfCheckId', required=True, help="selfCheck id")
@click.option('--emailList', 'emailList', required=True)
def update_self_check_watchers(selfCheckId, emailList):
    SelfCheckService().update_watchers(selfCheckId, emailList)
    print("Success: Update self-check watchers")


@update_partners.command('watchers')
@click.option('--partnerId', 'partnerId', required=True, help="partner id")
@click.option('--emailList', 'emailList', required=True)
def update_partners_watchers(partnerId, emailList):
    client = get_api_client()
    response = client.update_partners_watchers(
        partnersId=partnerId,
        emailList=emailList,
    )
    check_response(response)
    print("Success: Update partners watchers")
