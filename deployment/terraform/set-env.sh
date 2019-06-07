#!/bin/bash

DIR=$(pwd)
DATAFILE="$DIR/$1"

ENVIRONMENT=$(sed -nr 's/^environment\s*=\s*"([^"]*)".*$/\1/p' "$DATAFILE")
BUCKET=$(sed -nr 's/^bucket_name\s*=\s*"([^"]*)".*$/\1/p' "$DATAFILE")
DEPLOYMENT=$(sed -nr 's/^deployment_name\s*=\s*"([^"]*)".*$/\1/p' "$DATAFILE")
PROJECT=$(sed -nr 's/^project\s*=\s*"([^"]*)".*$/\1/p' "$DATAFILE")
CREDENTIALS=$(sed -nr 's/^credentials\s*=\s*"([^"]*)".*$/\1/p' "$DATAFILE")


if [ ! -f "$DATAFILE" ]; then
    echo "setenv: Configuration file not found: $DATAFILE"
    return 1
fi

if [ -z "$ENVIRONMENT" ]
then
    echo "setenv: 'environment' variable not set in configuration file."
    return 1
fi

if [ -z "$BUCKET" ]
then
  BUCKET='fuchicorp'
    echo "setenv: 'bucket_name' variable not set in configuration file."
fi

if [ -z "$PROJECT" ]
then
  PROJECT='fuchicorp-project'
    echo "setenv: 'project_name' variable not set in configuration file."
fi

if [ -z "$CREDENTIALS" ]
then
    echo "setenv: 'credentials' file not set in configuration file."
    return 1
fi

if [ -z "$DEPLOYMENT" ]
then
    echo "setenv: 'deployment_name' variable not set in configuration file."
    return 1
fi

cat << EOF > "$DIR/backend.tf"
terraform {
  backend "gcs" {
    bucket  = "${BUCKET}"
    prefix  = "${ENVIRONMENT}/${DEPLOYMENT}"
    project = "${PROJECT}"
  }
}
EOF


GOOGLE_APPLICATION_CREDENTIALS="${DIR}/${CREDENTIALS}"

export GOOGLE_APPLICATION_CREDENTIALS
export DATAFILE
rm -rf "$DIR/.terraform"

echo "setenv: Initializing terraform"
terraform init #> /dev/null
