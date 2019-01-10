#!/usr/bin/env python3
# -*-coding:utf-8-*-

from jinja2 import Environment, FileSystemLoader

from src.utils import resolve_path


file_loader = FileSystemLoader(resolve_path("templates_dockerfile"))
env = Environment(loader=file_loader)


params = {
    "login": "2015bernarda",
    "email_address": "aymeric.bernard@student.ecp.fr",
    "website_name": "autopython",

    "image": "python",
    "requirements_path": "requirements.txt",
    "build_script": None,
    "exposed_ports": [8042],
    "start_script": "python3 flaskserver.py"
}


template = env.get_template("python_3.7-slim-stretch.jinja2")
params["start_script"] = params["start_script"].split(" ")  # TODO
output = template.render(**params)


export_path = f"/dockerfiles/{params['login']}/{params['website_name']}/Dockerfile"
image_name = f"{params['login']}-{params['website_name']}-{params['image']}"

print(f"----- Should be saved in {export_path} -----")
print(output)
print(f"----------")
print(f"===== Image should be built with `docker build -t {image_name} .` -----")


if __name__ == "__main__":
    pass
