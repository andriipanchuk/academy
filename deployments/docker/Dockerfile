# Pulling default image from DockerHub
FROM python:latest

MAINTAINER Fuchi Corp fuchicorpsolutins@gmail.com

## Copy everything to image folder root
WORKDIR /app
COPY . /app

## Docker build is required argument "branch_name" value should be master|qa|dev
ARG branch_name
ENV BRANCH_NAME=$branch_name

## Create kube folder insied root Copy KuberConfig to the docker images
RUN mkdir /root/.kube


## Install all requirements to the docker image
RUN python -m pip install -r requirements.txt


## Expose the port 5000
EXPOSE 5000

## To run this docker image need commmand
# CMD ['python', '/app/app.py']
