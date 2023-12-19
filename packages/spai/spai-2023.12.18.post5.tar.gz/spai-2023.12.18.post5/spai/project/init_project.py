import shutil
from pathlib import Path
import os


def init_project(path, project_name):
    # copy template
    template = Path(__file__).parent / "project-template"
    shutil.copytree(template, path / project_name)
    # change name to project in spai.config.yaml
    config = path / project_name / "spai.config.json"
    os.system(f"sed -i 's/project-template/{project_name}/g' {config}")
