#!/usr/bin/env python3
# -*-coding:utf-8-*-

"""
Flask server to create and display Dockerfile and docker-compose.yml files
"""

import os
from glob import glob
from pprint import pprint
from typing import Dict, List, Any

from flask import Flask, request
from flask_socketio import SocketIO, emit
from jinja2 import Environment, FileSystemLoader

from src.utils import resolve_path
from src.choices import all_questions_dict, all_questions_json
from src.template_selector import template_selector


app = Flask(__name__)
socketio = SocketIO(app)


dockerfile_template_files = glob(resolve_path("templates_dockerfile", "*.jinja2"))
known_dockerfile_templates = [os.path.split(fn)[1][:-7] for fn in dockerfile_template_files]

docker_compose_template_files = glob(resolve_path("templates_docker_compose", "*.yml.jinja2"))
known_docker_compose_templates = [os.path.split(fn)[1][:-11] for fn in docker_compose_template_files]


default_params = {q.get("label"): q.get("default") for q in all_questions_dict}
print("--- Default params ---")
pprint(default_params)
print('--- ---')


# @app.route("/")
# def index():
#     return index_template.render(labels=labels, placeholders=placeholders)


@socketio.on("connect", namespace="/typhoon")
def test_connect():
    get_questions()


@socketio.on("disconnect", namespace="/typhoon")
def test_disconnect():
    print("Client disconnected", request.sid)


@socketio.on("questions", namespace="/typhoon")
def get_questions():
    emit("questions", {"data": all_questions_json})


@socketio.on("form_changed", namespace="/typhoon")
def form_changed(message):
    params: Dict[str, Any] = default_params.copy()

    for d in message["data"]:
        if d.get("label") in params:
            params[d.get("label")] = d.get("answer")

    params["start_script"] = params["start_script"].split(" ")  # TODO
    if params["exposed_ports"]:
        try:
            params["exposed_ports"] = [int(p) for p in params["exposed_ports"].split(",")]  # TODO
        except ValueError:
            params["exposed_ports"] = []

    dockerfile_template = None
    docker_compose_template = None
    template_data = template_selector.get(params["template"])
    if template_data:
        dockerfile_template = template_data.get("dockerfile")
        docker_compose_template = template_data.get("docker_compose")

    if dockerfile_template is not None and dockerfile_template not in known_dockerfile_templates:
        print(f"WARN: Invalid Dockerfile template: {dockerfile_template}")
        dockerfile_template = None

    if docker_compose_template is not None and docker_compose_template not in known_docker_compose_templates:
        print(f"WARN: Invalid docker_compose template: {docker_compose_template}")
        docker_compose_template = None

    dockerfile_output = "No Dockerfile"
    if dockerfile_template is not None:
        dockerfile_template = env_dockerfile.get_template(dockerfile_template + ".jinja2")
        dockerfile_output = dockerfile_template.render(**params)
    emit("dockerfile", {"data": dockerfile_output})

    docker_compose_output = "No docker-compose"
    if docker_compose_template is not None:
        docker_compose_template = env_docker_compose.get_template(docker_compose_template + ".yml.jinja2")
        docker_compose_output = docker_compose_template.render(**params)
    emit("docker_compose", {"data": docker_compose_output})


if __name__ == "__main__":
    env_server = Environment(loader=FileSystemLoader(resolve_path("templates_server")))
    env_dockerfile = Environment(loader=FileSystemLoader(resolve_path("templates_dockerfile")))
    env_docker_compose = Environment(loader=FileSystemLoader(resolve_path("templates_docker_compose")))

    index_template = env_server.get_template("index.html")

    socketio.run(app, host="0.0.0.0", port=8056, debug=True)