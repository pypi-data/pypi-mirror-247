import click

from src.client import get_api_client
from src.commands.base import cli
from src.services.project import ProjectService
from src.utils.json import pretty_print_dict
from src.utils.response import check_response


@cli.group()
def get():
    pass


@get.command("projects")
@click.option("--createDate", "createDate")
@click.option("--creator", "creator")
@click.option("--division", "division")
@click.option("--modelName", "modelName")
@click.option("--prjIdList", "prjIdList")
@click.option("--status", "status")
@click.option("--updateDate", "updateDate")
def get_projects(
    createDate,
    creator,
    division,
    modelName,
    prjIdList,
    status,
    updateDate,
):
    data = ProjectService().get(
        createDate=createDate,
        creator=creator,
        division=division,
        modelName=modelName,
        prjIdList=prjIdList,
        status=status,
        updateDate=updateDate,
    )
    pretty_print_dict(data)


@get.command("projectModels")
@click.option("--prjIdList", "prjIdList")
def get_project_models(prjIdList):
    data = ProjectService().get_models(prjIdList)
    pretty_print_dict(data)


@get.command("licenses")
@click.option("--licenseName", "licenseName", required=True, help="license name")
def get_licenses(licenseName):
    client = get_api_client()
    response = client.get_licenses(licenseName=licenseName)
    if response.status_code == 404:
        print("Not found")
        return
    check_response(response)
    pretty_print_dict(response.json())


@get.command("oss")
@click.option("--ossName", "ossName", required=True, help="oss name")
@click.option("--ossVersion", "ossVersion", help="oss version")
@click.option("--downloadLocation", "downloadLocation", help="download location")
def get_oss(ossName, ossVersion, downloadLocation):
    client = get_api_client()
    response = client.get_oss(
        ossName=ossName,
        ossVersion=ossVersion,
        downloadLocation=downloadLocation,
    )
    check_response(response)
    pretty_print_dict(response.json())


@get.command("partners")
@click.option("--createDate", "createDate")
@click.option("--creator", "creator")
@click.option("--division", "division")
@click.option("--partnerIdList", "partnerIdList")
@click.option("--status", "status")
@click.option("--updateDate", "updateDate")
def get_partners(
    createDate,
    creator,
    division,
    partnerIdList,
    status,
    updateDate,
):
    client = get_api_client()
    response = client.get_partners(
        createDate=createDate,
        creator=creator,
        division=division,
        partnerIdList=partnerIdList,
        status=status,
        updateDate=updateDate,
    )
    check_response(response)
    pretty_print_dict(response.json())


@get.command("maxVulnerability")
@click.option("--ossName", "ossName", required=True, help="oss name")
@click.option("--ossVersion", "ossVersion", help="oss version")
def get_max_vulnerability(ossName, ossVersion):
    client = get_api_client()
    response = client.get_max_vulnerability(ossName=ossName, ossVersion=ossVersion)
    check_response(response)
    pretty_print_dict(response.json())


@get.command("vulnerability")
@click.option("--cveId", "cveId", help="cve id")
@click.option("--ossName", "ossName", help="oss name")
@click.option("--ossVersion", "ossVersion", help="oss version")
def get_vulnerability(cveId, ossName, ossVersion):
    client = get_api_client()
    response = client.get_vulnerability(
        cveId=cveId,
        ossName=ossName,
        ossVersion=ossVersion,
    )
    check_response(response)
    pretty_print_dict(response.json())


@get.command("codes")
@click.option("--codeType", "codeType", required=True, help="code type")
@click.option("--detailValue", "detailValue", help="detail value")
def get_codes(codeType, detailValue):
    client = get_api_client()
    response = client.get_codes(codeType=codeType, detailValue=detailValue)
    check_response(response)
    pretty_print_dict(response.json())
