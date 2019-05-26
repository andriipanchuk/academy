# Pulling default image from DockerHub
FROM python:latest
MAINTAINER Farkhod Sadykov

## Copy everything to image folder root
WORKDIR /app
COPY . /app

ARG branch_name
ENV BRANCH_NAME=$branch_name

## Create kube folder insied root Copy KuberConfig to the docker images
RUN mkdir /root/.kube

# ## Set credentials for google cluster
# ENV GOOGLE_APPLICATION_CREDENTIALS=/root/.kube/flask-kube.json


## Install all requirements to the docker image
RUN python -m pip install -r requirements.txt

## Install gcloud in docker container
# RUN curl -sSL https://sdk.cloud.google.com | bash

## Expose the port 5000
EXPOSE 5000

## Install kubectl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl
RUN kubectl version 2>/dev/null

#WORKDIR /root/
## To run this docker image need commmand
# CMD ['python', '/app/app.py']
