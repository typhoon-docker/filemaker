"""
Scripts to write the docker files, build the image (and run the missile ?)
"""

import os
import time
import subprocess as sp
from typing import List, Dict, Any, Union, Callable

import src.utils as utils


def run_process_send_to_socket(cmd: Union[str, List[str]], callback: Callable[[str], None], **kwargs):
    """Run a process with the given `cmd`, will call the `callback` with each output line"""

    print(f">>> Will run: {cmd}")
    callback(f">>> Will run: {cmd}")

    # First, we open a handle to the external command to be run.
    # Then we send whatever output the command gave us back via the socket
    try:
        process = sp.Popen(cmd, stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.STDOUT, **kwargs)
    except Exception as e:
        print(f"Exception: {e}")
        callback(f"exception>>> {e}")
        return -1

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
        return -2
    finally:
        # Wrapping up
        process.stdin.close()
        process.stdout.close()

    print(f">>> Finished: {cmd} (exit code {process.returncode})")
    callback(f">>> Finished: {cmd} (exit code {process.returncode})")
    return process.returncode


def clone_or_pull_code(params: Dict[str, Any], callback: Callable[[str], None]):
    """Infer the cloning directory from `params`, check if we already have the project (pull) or not (clone)"""
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
    run_process_send_to_socket(cmd, callback, cwd=clone_dir)


def write_dockerfiles(dockerfile_output: List[Dict[str, str]]):
    """Write the dockerfiles in files. arg: {"image": image_name, "dockerfile": dockerfile_content}"""
    for ti in dockerfile_output:
        image = ti["image"]
        dockerfile = ti["dockerfile"]
        file_path = utils.get_dockerfile_path(image)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            print(f"Writing Dockerfile in {file_path}...")
            f.write(dockerfile)


def write_docker_compose(params: Dict[str, Any], docker_compose_output: str):
    """Write the docker-compose in a file. args: query params and docker-compose content"""
    file_path = utils.get_docker_compose_path(params)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        print(f"Writing docker_compose in {file_path}...")
        f.write(docker_compose_output)


def build_docker_image(params: Dict[str, Any], callback: Callable[[str], None]):
    """Use the code and dockerfile to build the image"""
    dockerfiles_info = utils.get_docker_templates(params).get("dockerfiles")
    for dockerfile in dockerfiles_info:
        img_name = dockerfile.get("image")
        df_path = utils.get_dockerfile_path(img_name)
        ctx = utils.get_dockerfile_context(params)
        run_process_send_to_socket(["docker", "build", "-t", img_name, "-f", df_path, "."], callback, cwd=ctx)


def docker_compose_up(params: Dict[str, Any], callback: Callable[[str], None]):
    """Call docker-compose up from the project's docker-compose directory"""
    # FIXME: this should most probably be done on the host machine itself, not on the docker we are in
    dc_path = utils.get_docker_compose_path(params)
    dc_dir = os.path.dirname(dc_path)
    # run_process_send_to_socket(["docker-compose", "down"], callback, cwd=dc_dir)
    # run_process_send_to_socket(["docker-compose", "up"], callback, cwd=dc_dir)


def build_and_run(params: Dict[str, Any], dockerfile_output: List[Dict[str, str]], docker_compose_output: str,
                  socket_callback: Callable[[str], None]):
    """Will call all the steps to build and run everything"""

    print("=== clone_or_pull_code ===")
    socket_callback("=== clone_or_pull_code ===")
    clone_or_pull_code(params, socket_callback)

    print("=== write_dockerfiles ===")
    socket_callback("=== write_dockerfiles ===")
    write_dockerfiles(dockerfile_output)

    print("=== write_docker_compose ===")
    socket_callback("=== write_docker_compose ===")
    write_docker_compose(params, docker_compose_output)

    print("=== build_docker_image ===")
    socket_callback("=== build_docker_image ===")
    build_docker_image(params, socket_callback)

    print("=== docker_compose_up ===")
    socket_callback("=== docker_compose_up ===")
    docker_compose_up(params, socket_callback)

    print("=== All done ===")
    socket_callback("=== All done ===")
