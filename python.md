# Python guidelines

Remember to read the general guidelines in the main README first!

Also see the [Standard Environment setup][stdenv], even though it says
Ubuntu you can use it on Windows thanks to [Windows Subsystem for Linux][wsl2].

[stdenv]: ./ubuntu2004_python3_setup.md
[wsl2]: ./win10_wsl2_docker.md

## Use python3

Use 3.9 as the bare minimum version.

Using 3.11 is recommended in general for everything that is not a library that must
work with legacy things.

## Use virtualenv

Specifically use [virtualenvwrapper][vew], it makes things very simple
and you can easily run stuff from terminal without having to fire up your
IDE just to get to your virtualenv.

[vew]: https://virtualenvwrapper.readthedocs.io/en/latest/

## Use [pep8][pep8] style

This is the official Python style. Black and pylint (see below) will
help you with this.

[pep8]: https://www.python.org/dev/peps/pep-0008/

## Start with a template

We have a [minimal template][minimalcc] which you should use unless
there's a more specific one for your use case available.

The template sets up your project with sane defaults for code-quality etc.

[minimalcc]: https://gitlab.com/advian-oss/python-lib_template

Most of the other stuff here is already set up correctly when using
one of our own templates.

## Use asyncio

While concurrency is not parallelism, using asyncio makes your code more efficient
and using threads manually is a sure-fire way to get very "interesting" bugs.

If you have computationally heavy things that are not asyncio-aware already you
should use [executors][blocking] to run them (asyncio will handle the threading stuff
for you).

For true parallelism use [ProcessPoolExecutor][ppe] that runs your
tasks in separate subprocesses (Python has this thing called Global Interpreter Lock
that limits how much true parallelism you can achieve with threading).

[blocking]: https://docs.python.org/3.8/library/asyncio-dev.html#running-blocking-code
[ppe]: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor

## Minimal dependencies

Especially: Don't use OpenCV or Numpy if you don't absolutely have to.
For simple image stuff there's always [Pillow][pillow].

These packages are huge and if precompiled wheels are not available for a given
target environment installing them is a giant pain.

Remember: the deployment env is never going to be identical to your
development laptop so "works on my machine" is not going to cut it.

[pillow]: https://pillow.readthedocs.io/en/stable/

## Unit test all the things

And use [`py.test`][pytest] to do it. Set your test framework to also
check for coverage and fail tests if some sensible level is not met.

It's a good idea to run the full test suite before committing but as
your suite grows this gets slow so it probably is not a good idea
to autorun it from a pre-commit hook.

[pytest]: https://docs.pytest.org/en/latest/

## Run your basic code-quality tools before committing

Using a pre-commit framework to enforce this is a good idea. However it's an
even better idea to run them manually first, when using the template make
sure all the files are added to git and then `pre-commit run --all-files`

Greatest reason for this is that some of the autoformatters etc will very
likely change your files and this will cause the commit to fail and then
you'd need to retype your commit messages (if not given via `-m`)

## Use tox

To run your test suite across multiple python versions easily.

There is a [Docker image][toxdocker] that makes this a bit simpler, or you
could set up pyenv yourself.

[toxdocker]: https://github.com/advian-oss/docker-pyenv-tox

## Use black

It auto-formats your code to a common standard.

## Use pylint

And keep it strict, see the minimal template above for good default config.

## Use type hints & mypy

And keep it strict. Type hinting will make future refactoring much safer
and it will save you from a bunch of bugs right now as well.

## Use pyproject.toml

This is the modern way to handle package metadata.

## Use [Poetry][poetry]

The modern packaging and dependency management tool.

[poetry]: https://python-poetry.org/

### Poetry pypi dependencies

`poetry add packagename` will add the dependency like this:

    packagename = "^1.2.3"

which lock the version to the minor version (only patch version can change)
for poetry update, you probably want to lock only major version so change
the version to `"^1.2"`.

### Poetry git dependencies

Make sure to use git tags for the dependencies::

    privatepackage = {git = "ssh://git@github.com/PVARKI-projekti/python-privatepackage", tag = "0.5.0"}

For development and testing purposes when you are developing the package you depend
to at the same time you can also use `branch = "mybranch"` but before merging your
changes to default branch make sure all git dependencies use tags (and remember to run
`poetry update` to make sure the lockfile is up-to-date)
