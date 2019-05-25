#!/bin/bash

shdirbase="$( dirname $0 )"
shdir="$( cd $shdirbase && pwd -P )"
scriptname="$( basename $0 )"

PROJECT_HOME="$( cd $shdir
while [[ ! -d .git ]]
do
  cd ..
done
pwd -P )"

PROJECT_NAME="${PROJECT_HOME##*/}"
BRANCH_NAME="$(git branch | grep \* | cut -d ' ' -f2)"

if [ "$0" = "$BASH_SOURCE" ]
then
    echo "$0: Please source this file."
    echo "e.g. source ./get-setenv.sh webplatform.tfvars"
    return 1
fi

if [[ $PROJECT_NAME == "webplatform" ]]; then
  terraform init \
    -backend-config "prefix=$PROJECT_NAME"_"$BRANCH_NAME" \
    -backend-config "bucket=fuchicorp"
else
  terraform init \
    -backend-config "prefix=$PROJECT_NAME"\
    -backend-config "bucket=fuchicorp"
fi
