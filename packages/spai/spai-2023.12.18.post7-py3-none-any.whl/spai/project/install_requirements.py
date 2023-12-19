import os


def install_requirements(config, logger=print):
    # install requirements.txt in each service folder
    for service in config:
        logger(f"Installing requirements for service '{service.name}'...")
        service_path = config.dir / config.type2folder(service.type) / service.name
        reqs_path = service_path / "requirements.txt"
        if not reqs_path.exists():
            logger(f"No requirements.txt found for service '{service.name}'.")
            continue
        os.system(f"pip install -r {str(reqs_path)}")
    return "done"
