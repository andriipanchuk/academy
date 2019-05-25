#!/bin/bash

shdirbase="$( dirname $0 )"
shdir="$( cd $shdirbase && pwd -P )"
scriptname="$( basename $0 )"

PROJECT_NAME="webplatform"

PROJECT_HOME="$( cd $shdir
while [[ ! -d .git ]]
do
  cd ..
done
pwd -P )"


if [[ $1 -eq 0 ]] ; then
    BRANCH_NAME="$1"
else
  BRANCH_NAME="$(git branch | grep \* | cut -d ' ' -f2)"
fi


if [ "$0" = "$BASH_SOURCE" ]
then
    echo "$0: Please source this file."
    echo "e.g. source ./get-setenv.sh webplatform.tfvars"
    return 1
fi

terraform init \
  -backend-config "prefix=$PROJECT_NAME"_"$BRANCH_NAME" \
  -backend-config "bucket=fuchicorp"
