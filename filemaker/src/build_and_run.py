"""
Scripts to build the docker files and run the missile
"""

import os
import time
import subprocess as sp
from typing import List, Dict, Any, Union, Callable

import src.utils as utils


def run_process_send_to_socket(cmd: Union[str, List[str]], callback: Callable[[str], None], **kwargs):
    print(f">>> Will run: {cmd}")
    callback(f">>> Will run: {cmd}")

    # First, we open a handle to the external command to be run.
    # Then we send whatever output the command gave us back via the socket
    try:
        process = sp.Popen(cmd, stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.STDOUT, **kwargs)
    except Exception as e:
        print(f"Exception: {e}")
        callback(f"exception>>> {e}")
        return

    # Wait for the command to finish
    # (.poll() will return the exit code, None if it's still running)
    while process.poll() is None:
        time.sleep(0.025)

    # Then we send whatever output the command gave us back via the socket
    try:
        line = process.stdout.read().decode("utf-8")
        print(f"process>>> {line}")
        callback(f"process>>> {line}")
    except Exception as e:
        print(f"Exception: {e}")
        callback(f"exception>>> {e}")

    process.stdin.close()
    process.stdout.close()

    print(f">>> Finished: {cmd}")
    callback(f">>> Finished: {cmd}")


def clone_or_pull_code(params: Dict[str, Any], callback: Callable[[str], None]):
    clone_dir = utils.get_clone_path(params)
    os.makedirs(clone_dir, exist_ok=True)
    if os.path.exists(os.path.join(clone_dir, ".git")):
        print("Directory exists, pulling new code")
        callback("Directory exists, pulling new code")
        cmd = ["git", "pull"]
    else:
        print("Directory not found, cloning")
        callback("Directory not found, cloning")
        cmd = ["git", "clone", params["repository_url"], clone_dir]
    return cmd, clone_dir


def write_dockerfiles(dockerfile_output: List[Dict[str, str]]):
    for ti in dockerfile_output:
        image = ti["image"]
        dockerfile = ti["dockerfile"]
        file_path = utils.get_dockerfile_path(image)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            print(f"Writing Dockerfile in {file_path}...")
            f.write(dockerfile)


def write_docker_compose(params: Dict[str, Any], docker_compose_output: str):
    file_path = utils.get_docker_compose_path(params)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        print(f"Writing docker_compose in {file_path}...")
        f.write(docker_compose_output)


def build_docker_image(params: Dict[str, Any], callback: Callable[[str], None]):
    dockerfiles_info = utils.get_docker_templates(params).get("dockerfiles")
    for dockerfile in dockerfiles_info:
        img_name = dockerfile.get("image")
        df_path = utils.get_dockerfile_path(img_name)
        ctx = utils.get_dockerfile_context(params)
        # TODO
        # go to ctx
        # docker build -t img_name -f df_path .
        run_process_send_to_socket(["docker", "build", "-t", img_name, "-f", df_path, "."], callback, cwd=ctx)


def docker_compose_up(params: Dict[str, Any], callback: Callable[[str], None]):
    dc_path = utils.get_docker_compose_path(params)
    dc_dir = os.path.dirname(dc_path)
    # TODO
    # go to dc_path's directory
    # docker-compose up
    # run_process_send_to_socket(["docker-compose", "down"], callback, cwd=dc_dir)
    # run_process_send_to_socket(["docker-compose", "up"], callback, cwd=dc_dir)


def build_and_run(params: Dict[str, Any], dockerfile_output: List[Dict[str, str]], docker_compose_output: str,
                  socket_callback: Callable[[str], None]):
    cmd, clone_dir = clone_or_pull_code(params, socket_callback)
    print("=== clone_or_pull_code ===")
    socket_callback("=== clone_or_pull_code ===")
    run_process_send_to_socket(cmd, socket_callback, cwd=clone_dir)

    print("=== write_dockerfiles ===")
    socket_callback("=== write_dockerfiles ===")
    write_dockerfiles(dockerfile_output)

    print("=== write_docker_compose ===")
    socket_callback("=== write_docker_compose ===")
    write_docker_compose(params, docker_compose_output)

    # TODO build Docker image
    print("=== build_docker_image ===")
    socket_callback("=== build_docker_image ===")
    build_docker_image(params, socket_callback)

    # TODO docker-compose up ?? (Needs down as well)
    print("=== docker_compose_up ===")
    socket_callback("=== docker_compose_up ===")
    docker_compose_up(params, socket_callback)

    print("=== All done ===")
    socket_callback("=== All done ===")
