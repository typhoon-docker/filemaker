import os
from typing import Dict, Any, Optional

import config


_orig_dir = os.path.dirname(os.path.realpath(__file__))


def resolve_path(*path: str):
    """Resolve any path based on the project root.
    resolve_path('foo', 'bar') will give an absolute path to your_project_directory/foo/bar
    If the path is already absolute, it will stay absolute
    """
    return os.path.abspath(os.path.join(_orig_dir, '..', *path))


def get_docker_templates(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """For each supported template, returns the dockerfile docker-compose templates to use"""

    if params["template"] == "static":
        return {"dockerfiles": [],
                "docker_compose": "static",
                }

    if params["template"] == "python":
        return {"dockerfiles": [{"template": "python_3.7-slim-stretch",
                                 "image": f"{params['login']}-{params['website_name']}-python"}],
                "docker_compose": "python",
                }

    if params["template"] == "php":
        return {"dockerfiles": [{"template": "php_7.3-apache",
                                 "image": f"{params['login']}-{params['website_name']}-php"}],
                "docker_compose": "php",
                }

    if params["template"] == "react":
        return {"dockerfiles": [{"template": "built_node_8.15-alpine",
                                 "image": f"{params['login']}-{params['website_name']}"}],
                "docker_compose": "standalone",
                }

    return None


def get_clone_path(params: Dict[str, Any]):
    """Returns the directory in which the repo will be cloned"""
    return os.path.join(config.CLONE_ROOT, params["login"], params["website_name"])


def get_dockerfile_context(params: Dict[str, Any]):
    """Returns the directory from where the docker image should be built (important since path are relative)"""
    if params["root_folder"]:
        return os.path.join(get_clone_path(params), params["root_folder"])
    return get_clone_path(params)


def get_dockerfile_path(image_name: str):
    """Returns the path to the Dockerfile"""
    return os.path.join(config.DOCKERFILE_ROOT, image_name, "Dockerfile")


def get_docker_compose_path(params: Dict[str, Any]):
    """Returns the path to the docker-compose.yml file"""
    return os.path.join(config.DOCKER_COMPOSE_ROOT, f"{params['login']}-{params['website_name']}", "docker-compose.yml")
