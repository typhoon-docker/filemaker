"""
Scripts to build the docker files and run the missile
"""

import os
import time
import subprocess as sp
from typing import List, Dict, Any, Union, Callable

import src.utils as utils


def run_process_send_to_socket(cmd: Union[str, List[str]], callback: Callable[[str], None]):
    callback(f">>> Will run: {cmd}")

    # First, we open a handle to the external command to be run.
    process = sp.Popen(cmd, stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.STDOUT)

    # Wait for the command to finish
    # (.poll() will return the exit code, None if it's still running)
    while process.poll() is None:
        time.sleep(0.025)

    # Then we send whatever output the command gave us back via the socket
    try:
        callback(process.stdout.read().decode("utf-8"))
    except Exception as e:
        pass

    process.stdin.close()
    process.stdout.close()


def clone_or_pull_code(params):
    clone_dir = utils.get_clone_path(params)
    os.makedirs(clone_dir, exist_ok=True)
    if os.path.exists(os.path.join(clone_dir, ".git")):
        cmd = ["git", "pull"]
    else:
        cmd = ["git", "clone", params["repository_url"]]
    return cmd


def write_dockerfile(params, dockerfile_output):
    file_path = utils.get_dockerfile_path(params)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(dockerfile_output)


def write_docker_compose(params, docker_compose_output):
    file_path = utils.get_docker_compose_path(params)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(docker_compose_output)


def build_docker_image(params):
    dockerfiles_info = utils.get_docker_templates(params).get("dockerfiles")
    for dockerfile in dockerfiles_info:
        img_name = dockerfile.get("image")
        img_path = utils.get_dockerfile_path(img_name)
        # TODO


def docker_compose_up(params):
    dc_path = utils.get_docker_compose_path(params)
    # TODO


def build_and_run(params: Dict[str, Any], dockerfile_output: str, docker_compose_output: str,
                  socket_callback: Callable[[str], None]):
    cmd0 = clone_or_pull_code(params)
    socket_callback("=== clone_or_pull_code ===")
    run_process_send_to_socket(cmd0, socket_callback)
    socket_callback("\n")

    write_dockerfile(params, dockerfile_output)
    write_docker_compose(params, docker_compose_output)

    cmd0 = clone_or_pull_code(params)
    socket_callback("=== clone_or_pull_code ===")
    run_process_send_to_socket(cmd0, socket_callback)
    socket_callback("\n")
