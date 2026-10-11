#!/bin/bash -l
set -e
if [ "$#" -eq 0 ]; then
  pandoc -o pvarki_best_practises.pdf \
    --filter mermaid-filter \
    --pdf-engine=wkhtmltopdf \
    --from gfm \
    README.md \
    rationality/README.md \
    tools/git.md \
    tools/ci.md \
    tools/logging.md \
    tools/databases.md \
    tools/ssh_tips.md \
    frameworks-languages/python.md \
    frameworks-languages/typescript.md \
    frameworks-languages/rust.md \
    frameworks-languages/c_and_cpp.md \
    agents/README.md \
  && rm mermaid-filter.*
else
  exec "$@"
fi
