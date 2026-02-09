#!/bin/bash

IMAGE_NAME="gria2526-abia"

sudo docker run  -e NB_UID=$(id -u) -e NB_GID=$(id -g) -e CHOWN_HOME=yes -e CHOWN_HOME_OPTS='-R' -it --rm --name="AIBA" -v "${PWD}":/home/jovyan/work  -p 8888:8888 ${IMAGE_NAME} start-notebook.sh --ServerApp.token=''

