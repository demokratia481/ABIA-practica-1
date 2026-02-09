#!/bin/bash

IMAGE_NAME="gria2526-abia"

# Build
docker build -t ${IMAGE_NAME} .

#In Linux Ubuntu Noble with latest official Docker Engine use the following command:
#docker buildx build -t ${IMAGE_NAME} .

