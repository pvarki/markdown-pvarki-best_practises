#!/bin/bash -l
if [ ! -d .git ]
then
  git init
  git checkout -b precommit_init
  git add .
fi
set -e
pre-commit install
pre-commit run --all-files
