"""
Maps the answer to the "template" question to the dockerfile and docker-compose templates to use
"""

template_selector = {
    "static": {
        "dockerfile": None,
        "docker_compose": "static"
    },
    "python": {
        "dockerfile": "python_3.7-alpine",
        "docker_compose": "python"
    },
    "php": {
        "dockerfile": "php_7.3-apache",
        "docker_compose": "php"
    },
}
