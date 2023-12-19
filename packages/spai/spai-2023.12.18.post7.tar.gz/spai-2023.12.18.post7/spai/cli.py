import typer
import os
import sys
from pathlib import Path
from . import __version__

# Add the cli directory to the Python path
# spai_cli_dir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(os.path.join(spai_cli_dir))

from .commands import auth as _auth

# from commands.src.usecases.auth import auth
# from commands.src.usecases.project import (
#     init_project,
#     install_reqs,
#     get_services,
#     stop_service,
#     get_logs,
# )
# from commands.src.usecases.run import (
#     run_local,
#     deploy_cloud,
#     load_and_validate_config,
# )

from .project import init_project, install_requirements, run_local
from .config import load_and_validate_config

app = typer.Typer(help="Welcome to SPAI")
app.add_typer(_auth.app, name="auth")


@app.command()
def init(path: Path = typer.Option(Path.cwd(), "-p", "--path", help="Project path")):
    project_name = typer.prompt("Projec name")
    init_project(path, project_name)
    typer.echo(f"Project {project_name} created at {path}")


# install requirements, should be executed in the project folder
@app.command()
def install(
    path: Path = typer.Option(Path.cwd(), "-p", "--path", help="Project path"),
    verbose: bool = typer.Option(False, "-v", "--verbose"),
):
    config = load_and_validate_config(path, typer, verbose)
    install_requirements(config, typer.echo)


@app.command()
def run(path: Path = typer.Option(Path.cwd(), "-p", "--path", help="Project path")):
    config = load_and_validate_config(path, typer)
    return run_local(path, config, typer)


# @app.command()
# def deploy(
#     dir: Path = typer.Option(
#         Path.cwd(), "-d", "--dir", help="Directory containing the spai.config.json file"
#     ),
#     rebuild: bool = typer.Option(False, "-r", "--rebuild"),  # force rebuild image
# ):
#     dir = Path(dir).resolve()
#     config = load_and_validate_config(dir, typer, True)
#     user = auth()
#     return deploy_cloud(user, dir, config, typer, rebuild)

# @app.command()
# def list(
#     project: str,
# ):
#     try:
#         user = auth()
#         services = get_services(user, project)
#         if len(services) == 0:
#             return typer.echo(f"No services running in project '{project}'.")
#         return typer.echo(f"Services in project '{project}': {services}")
#     except Exception as e:
#         return typer.echo(e)

# @app.command()
# def logs(
#     project: str,
#     service: str,
# ):
#     service, name = service.split(".")
#     user = auth()
#     logs = get_logs(user, project, service, name)
#     typer.echo(logs)

# @app.command()
# def stop(
#     project: str,
# ):
#     try:
#         user = auth()
#         services = get_services(user, project)
#         if len(services) == 0:
#             return typer.echo(f"No services running in project '{project}'.")
#         for service in services:
#             service_type, name = service.split(".")
#             typer.echo(f"Stopping service '{name}'...")
#             stop_service(user, project, service_type, name)
#         return typer.echo(f"Stopped all scripts in project '{project}'.")
#     except Exception as e:
#         return typer.echo(e)


@app.command()
def version():
    typer.echo(f"SPAI Version: {__version__}")


if __name__ == "__main__":
    app()
