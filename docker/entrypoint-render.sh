#!/bin/bash -l
set -e
if [ "$#" -eq 0 ]; then
  pandoc -o pvarki_best_practises.pdf \
    --filter mermaid-filter \
    --pdf-engine=wkhtmltopdf \
    --from gfm \
    README.md \
    git.md \
    ssh_tips.md \
    python.md \
    rust.md \
    c_and_cpp.md \
  && rm mermaid-filter.*
else
  exec "$@"
fi
