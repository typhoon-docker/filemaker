#!/usr/bin/env python3
# -*-coding:utf-8-*-

"""
Flask server to create and display Dockerfile and docker-compose.yml files
"""

from flask import Flask
from flask_socketio import SocketIO, emit

from src.choices import all_questions_json
from src.make_docker_files import make_dockerfiles_and_docker_compose
from src.build_and_run import build_and_run


app = Flask(__name__)
socketio = SocketIO(app)


# @app.route("/")
# def index():
#     return index_template.render(labels=labels, placeholders=placeholders)


@socketio.on("connect", namespace="/typhoon")
def test_connect():
    get_questions()


@socketio.on("disconnect", namespace="/typhoon")
def test_disconnect():
    print("Client disconnected")


@socketio.on("questions", namespace="/typhoon")
def get_questions():
    emit("questions", {"data": all_questions_json})


@socketio.on("form_changed", namespace="/typhoon")
def form_changed(message):
    params_dfs_and_dc = make_dockerfiles_and_docker_compose(message.get("data", []))
    params = params_dfs_and_dc["params"]
    dockerfiles_output = params_dfs_and_dc["dockerfiles"]
    docker_compose_output = params_dfs_and_dc["docker_compose"]

    # Send through socket
    emit("dockerfile", {"data": dockerfiles_output})
    emit("docker_compose", {"data": docker_compose_output})

    if message.get("validation", False):
        build_and_run(params, dockerfiles_output, docker_compose_output, lambda x: emit("log", {"message": x}))


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8056, debug=True)
