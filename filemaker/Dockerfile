FROM python:3.7-slim-stretch

# Setup
RUN mkdir /typhoon
WORKDIR /typhoon

# System package requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Python package requirements
COPY ./requirements.txt /typhoon/requirements.txt

RUN pip3 install -U pip --no-cache-dir && pip3 install -r /typhoon/requirements.txt --no-cache-dir

# Python source code
COPY . /typhoon

# Volumes
VOLUME /typhoon_sites
VOLUME /typhoon_dockerfile
VOLUME /typhoon_docker_compose
VOLUME /typhoon_volumes

# Expose the ports for the Flask server
EXPOSE 8056

# Set up Python path
ENV PYTHONPATH "/typhoon"

# Launch the script which will run the server
CMD ["python3", "src/server.py"]
