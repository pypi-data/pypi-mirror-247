import os
import json
from ...models import Config


def validate_folder(dir, folder, typer):
    if not os.path.exists(dir / folder):
        raise typer.BadParameter(f"No {folder} directory found in '{dir}'.")


def validate_item(dir, folder, item, name, typer, file="main.py"):
    # check name
    if not item.name:
        raise typer.BadParameter(f"{name} '{item.name}' is missing 'name' attribute.")
    # check folder has folder with item name
    if not os.path.exists(dir / folder / item.name):
        raise typer.BadParameter(
            f"{name} '{item.name}' cannot be found in {dir}/{folder}."
        )
    # check folder has file
    if not file in os.listdir(dir / folder / item.name):
        raise typer.BadParameter(f"{name} '{item.name}' is missing file 'main.py'.")
    # TODO: check optionals: reqs, env...


def load_and_validate_config(dir, typer, cloud=False):
    # check dir exists
    if not dir.exists():
        raise typer.BadParameter(f"Directory '{dir}' does not exist.")
    # check dir is a spai project
    if not "spai.config.json" in os.listdir(dir):
        raise typer.BadParameter(
            f"Directory '{dir}' is not a spai project. No spai.config.json file found."
        )
    # load config
    config = {}
    with open(dir / "spai.config.json", "r") as f:
        config = json.load(f)
    if not config:
        raise typer.BadParameter(f"spai.config.json file is empty.")
    services_config = config['services']
    services_config.update({"dir": dir})
    config = Config(**services_config)
    # TODO: check if project name is already taken in cloud, locally is not a problem
    config.project = dir.name if not config.project else config.project
    # check scripts
    if config.scripts:
        # check project has scripts folder
        validate_folder(dir, "scripts", typer)
        for _, script in config.scripts.items():
            validate_item(dir, "scripts", script, "script", typer)
    else:
        typer.echo("No scripts found in spai.config.json.")
    # check notebooks
    if config.notebooks:
        # check project has notebooks folder
        validate_folder(dir, "notebooks", typer)
        for _, notebook in config.notebooks.items():
            validate_item(dir, "notebooks", notebook, "notebook", typer, "main.ipynb")
    # check apis
    if config.apis:
        # check project has apis folder
        validate_folder(dir, "apis", typer)
        for _, api in config.apis.items():
            validate_item(dir, "apis", api, "api", typer)
    # check uis
    if config.uis:
        # check project has uis folder
        validate_folder(dir, "uis", typer)
        for _, ui in config.uis.items():
            validate_item(dir, "uis", ui, "ui", typer)
    return config
