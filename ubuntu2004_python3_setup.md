# Standard Py3 env on Ubuntu 20.04

If you are on Windows, use [WSL2][wsl2] to run this stuff.

[wsl2]: ./win10_wsl2_docker.md

## One time preparation

### Install Python3

    sudo apt-get update
    sudo apt-get install python3 python3-pip

### Install virtualenvwrapper

    pip3 install --user virtualenvwrapper
    echo 'export PATH=$HOME/.local/bin:$PATH' >>~/.profile
    echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3' >>~/.profile
    echo 'source $HOME/.local/bin/virtualenvwrapper.sh' >>~/.profile
    source ~/.profile

### Install Poetry

The "vendored" version is recommended by Poetry itself.

    curl -sSL https://install.python-poetry.org | python3 -

### Install other tools

These are good to have available globally under your user

    pip3 install --user git-up pre-commit cookiecutter

### Setup SSH keys

See [SSH tips & tricks][sshtips] document.

[sshtips]: ./ssh_tips.md

## For each project

Here we assume the project name is "mycoolapp"

### Create project virtualenv

    mkvirtualenv mycoolapp

The environment will be created and activated, to activate
it again later (or in another shell window) just use

    workon mycoolapp

### Use Cookiecutter to create the project

See the template you are going to use for details.

### Setup PyCharm to use the correct env

If on native Linux (or running PyCharm under WSL) then
you should be able to just choose from the existing virtualenvs.
If the list is not up-to-date the correct path can be seen
with command:

    which python3

When the virtualenv is activated.

On Windows TBD
