#!/usr/bin/env python3
# -*-coding:utf-8-*-

from jinja2 import Environment, FileSystemLoader

from src.utils import resolve_path


file_loader = FileSystemLoader(resolve_path("templates_docker_compose"))
env = Environment(loader=file_loader)


params = {
    "login": "2015bernarda",
    "email_address": "aymeric.bernard@student.ecp.fr",
    "website_name": "autopython",

    "requirements_path": "requirements.txt",
    "build_script": None,
    "exposed_ports": [8042],
    "start_script": "python3 flaskserver.py"
}


template = env.get_template("python.yml.jinja2")
output = template.render(**params)


export_path = f"/dockerfiles/{params['login']}/{params['website_name']}/docker-compose.yml"

print(f"----- Should be saved in {export_path} -----")
print(output)
print(f"----------")


if __name__ == "__main__":
    pass
