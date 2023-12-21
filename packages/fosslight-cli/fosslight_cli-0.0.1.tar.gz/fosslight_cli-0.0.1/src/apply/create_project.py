from typing import List

from src.services.project import ProjectService


def create_project(data: dict):
    service = ProjectService()

    # check schema
    required = [
        "parameters",
        "parameters.prjName",
        "parameters.osType",

        "update.models.modelListToUpdate",
        "update.modelFile.modelReport",
        "update.watchers.emailList",

        "scan.dir",
    ]
    for field in required:
        keys = field.split(".")
        if len(keys) == 1:
            assert _has_key(data, keys), f"SchemaError: createProject.{field} required"
        else:
            if _has_key(data, keys[:-1]):
                assert _has_key(data, keys), f"SchemaError: createProject.{field} required"

    # create
    prjId = service.create(**data["parameters"])
    print(f"Project created ({prjId})")

    # update
    if update := data["update"]:
        if models := update.get("models"):
            service.update_models(prjId=prjId, modelListToUpdate=models["modelListToUpdate"])
        if model_file := update.get("modelFile"):
            service.update_model_file(prjId=prjId, modelReport=model_file["modelReport"])
        if watchers := update.get("watchers"):
            service.update_watchers(prjId=prjId, emailList=watchers["emailList"])
        print(f"Project updated")

    # scan
    if scan := data["scan"]:
        service.scan(prjId=prjId, dir=scan["dir"])


def _has_key(data: dict, key_list: List[str]):
    result = data
    for key in key_list:
        result = result.get(key)
        if result is None:
            return False
    return True
