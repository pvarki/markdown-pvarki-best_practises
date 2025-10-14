#0############
# Run tests #
#############
FROM python:3.8-slim-buster as test
ENV \
  # locale
  LC_ALL=C.UTF-8 \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # debconf
  DEBIAN_FRONTEND=noninteractive

COPY . /app
WORKDIR /app
RUN --mount=type=ssh apt-get update \
    && apt-get install -y \
        curl \
        git \
        tini \
        openssh-client \
        # pre-commit needs to be able to build extensions
        build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    # Install pre-commit
    && pip3 install pre-commit \
    # check pre-commit stuff
    && docker/pre_commit_init.sh \
    && true
ENTRYPOINT ["/usr/bin/tini", "--", "docker/entrypoint-test.sh"]

#0####################
# deps for rendeding #
######################
FROM test as render_build
RUN --mount=type=ssh curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get update \
    && apt-get install -y \
        pandoc \
        wkhtmltopdf \
        chromium \
        yarn \
    && npm install --global mermaid-filter \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && true
ENTRYPOINT ["/bin/bash", "-l"]

FROM render_build as render
ENTRYPOINT ["/usr/bin/tini", "--", "docker/entrypoint-render.sh"]
