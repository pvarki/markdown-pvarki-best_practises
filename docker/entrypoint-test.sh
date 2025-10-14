#!/bin/bash -l
set -e
if [ "$#" -eq 0 ]; then
  pre-commit run --all-files
else
  exec "$@"
fi
