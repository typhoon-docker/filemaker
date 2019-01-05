#!/usr/bin/env python3
# -*-coding:utf-8-*-

"""
Will create the docker files from the templates, with the given answers
"""

import os
from glob import glob
import shlex
from pprint import pprint
from typing import Dict, Any

from jinja2 import Environment, FileSystemLoader

from src.utils import resolve_path, get_docker_templates
from src.choices import all_questions_dict


# Search templates in project files
dockerfile_template_files = glob(resolve_path("templates_dockerfile", "*.jinja2"))
docker_compose_template_files = glob(resolve_path("templates_docker_compose", "*.yml.jinja2"))

# Only keep the base name (no extension)
known_dockerfile_templates = [os.path.split(fn)[1][:-7] for fn in dockerfile_template_files]
known_docker_compose_templates = [os.path.split(fn)[1][:-11] for fn in docker_compose_template_files]

# Prepare the jinja2 FileSystemLoader
env_dockerfile = Environment(loader=FileSystemLoader(resolve_path("templates_dockerfile")))
env_docker_compose = Environment(loader=FileSystemLoader(resolve_path("templates_docker_compose")))

# Default answers to all the questions
default_params = {q.get("label"): q.get("default") for q in all_questions_dict}


def make_dockerfiles_and_docker_compose(message_data):
    """
    { "params": all the params, after transformation,
      "dockerfiles": list of {"image": "image_name", "dockerfile": "content"},
      "docker_compose": "content" }
    """
    params: Dict[str, Any] = default_params.copy()

    for d in message_data:
        if d.get("label") in params:
            params[d.get("label")] = d.get("answer")

    # Search for the right templates
    dockerfile_template_and_img = []
    docker_compose_template = None
    template_data = get_docker_templates(params)
    if template_data:
        dockerfile_template_and_img = template_data.get("dockerfiles")
        docker_compose_template = template_data.get("docker_compose")

    # Check if the selected template exists
    for ti in dockerfile_template_and_img:
        if ti.get("template") not in known_dockerfile_templates:
            print(f"WARN: Invalid Dockerfile template: {ti.get('template')}")
            ti["template"] = None

    if docker_compose_template is not None and docker_compose_template not in known_docker_compose_templates:
        print(f"WARN: Invalid docker_compose template: {docker_compose_template}")
        docker_compose_template = None

    # Cut the start script: 'python "my server.py"' -> '["python", "my server.py"]'
    try:
        params["start_script"] = "[" + ", ".join(f'"{a}"' for a in shlex.split(params["start_script"])) + "]"
    except Exception as e:
        params["start_script"] = f"[]  # Error: {e}"

    # Cut the exposed ports
    if params["exposed_ports"]:
        ports = []
        for p in params["exposed_ports"].split(","):
            try:
                ports.append(int(p))
            except ValueError:
                pass
        params["exposed_ports"] = ports

    # Cut the PYTHONPATH additions
    if params["add_to_pythonpath"]:
        params["add_to_pythonpath"] = params["add_to_pythonpath"].split(":")

    # Cut the js dependencies_files
    if params["dependencies_files"]:
        params["dependencies_files"] = params["dependencies_files"].split(":")

    # Create the Dockerfile content
    dockerfiles_output = []
    for ti in dockerfile_template_and_img:
        dockerfile_template = env_dockerfile.get_template(ti["template"] + ".jinja2")
        dockerfile = dockerfile_template.render(**params)
        dockerfiles_output.append({"image": ti["image"], "dockerfile": dockerfile})

    # Create the docker-compose content
    docker_compose_output = "No docker-compose"
    if docker_compose_template is not None:
        docker_compose_template = env_docker_compose.get_template(docker_compose_template + ".yml.jinja2")
        docker_compose_output = docker_compose_template.render(**params)

    # dockerfiles: list of {image: image_name, dockerfile: content}
    # docker_compose: content
    return {"params": params, "dockerfiles": dockerfiles_output, "docker_compose": docker_compose_output}


if __name__ == "__main__":
    print("--- Default params ---")
    pprint(default_params)
    print('--- ---')
