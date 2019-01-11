#!/usr/bin/env python3
# -*-coding:utf-8-*-

"""
Project entrypoint.
Flask server to create and display Dockerfile and docker-compose.yml files.
"""

from typing import List, Dict, Any

from flask import Flask
from flask_socketio import SocketIO, emit

from src.choices import all_questions_json
from src.make_docker_files import make_dockerfiles_and_docker_compose
from src.build_and_run import build_and_run


app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on("connect", namespace="/typhoon")
def test_connect():
    """Called when a client connects to the socket"""
    get_questions()
    emit("log", {"message": "You are connected."})


@socketio.on("disconnect", namespace="/typhoon")
def test_disconnect():
    """Called when a client disconnects from the socket"""
    print("Client disconnected")


@socketio.on("questions", namespace="/typhoon")
def get_questions():
    """Called when a client requests the list of questions"""
    emit("questions", {"data": all_questions_json})


@socketio.on("form_changed", namespace="/typhoon")
def form_changed(message):
    """Called when a client edits the form, with `validation` = true when clicked on the Send button"""
    params_dfs_and_dc = make_dockerfiles_and_docker_compose(message.get("data", []))
    params: Dict[str, Any] = params_dfs_and_dc["params"]
    dockerfiles_output: List[Dict[str, str]] = params_dfs_and_dc["dockerfiles"]
    docker_compose_output: str = params_dfs_and_dc["docker_compose"]

    # Send through socket
    emit("dockerfile", {"data": dockerfiles_output})
    emit("docker_compose", {"data": docker_compose_output})

    if message.get("validation", False):
        build_and_run(params, dockerfiles_output, docker_compose_output, lambda x: emit("log", {"message": x}))


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8056)
