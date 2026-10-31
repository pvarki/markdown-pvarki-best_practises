# Python guidelines

Remember to read the general guidelines in the main README first!

Also see the [Standard Environment setup][stdenv], even though it says
Ubuntu you can use it on Windows thanks to [Windows Subsystem for Linux][wsl2].

[stdenv]: ./ubuntu2004_python3_setup.md
[wsl2]: ./win11_wsl2_docker.md

## Use a supported python3 version

When setting up a new project, refer to the official [Python Developer's Guide][pydevguide]
and select a version with active support (`bugfix` mostly, otherwise `security` if it still
has 2+ years before EOL). The minimal template tracks this for you. If your project will be
deployed on cloud, remember to also check the versions supported by the cloud provider (e.g.
[Azure functions][azfunc]) and its SDK libraries, it might take some time before they support
the latest Python.

**Never** use a Python version that is EOL. EOL for Python usually comes in October, so plan
the migration to a newer version before the summer. First make sure your test suite runs also
on the newer Python version, tox (see below) makes running it on multiple versions easy.

[pydevguide]: https://devguide.python.org/versions/
[azfunc]: https://azure.microsoft.com/en-us/products/functions
q
## Use virtualenv

For projects uv (see below) creates and manages the `.venv` for you, just
`uv sync` and point your IDE to it. For ad-hoc environments outside of a
project [virtualenvwrapper][vew] still makes things very simple and you can
easily run stuff from terminal without having to fire up your IDE just to
get to your virtualenv.

[vew]: https://virtualenvwrapper.readthedocs.io/en/latest/

## Use [pep8][pep8] style

This is the official Python style. Ruff (see below) will
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

## Never use print(), always use logging facility

Nothing is more permanent than "temporary solution".

Always use the logging facility for debug messages. It's **two lines**
of code to set up (and our templates do it for you in the files they create)
and then a trivial amount of more characters to write per message (most which your
IDE will autocomplete anyway).

## Minimal dependencies

Especially: Don't use OpenCV or Numpy if you don't absolutely have to.
For simple image stuff there's always [Pillow][pillow].

These packages are huge and if precompiled wheels are not available for a given
target environment installing them is a giant pain.

Remember: the deployment env is never going to be identical to your
development laptop so "works on my machine" is not going to cut it.

[pillow]: https://pillow.readthedocs.io/en/stable/

## Test all the things

And use [`py.test`][pytest] to do it. The same rules for clean code also apply
to tests (readable, DRY etc.), make use of fixtures and parametrization.

Keep a clear separation between test types and follow the test pyramid: many
fast unit tests at the base, some functional/integration tests and a small set
of end-to-end tests at the top.

It's a good idea to run the full test suite before committing but as
your suite grows this gets slow so it probably is not a good idea
to autorun it from a pre-commit hook.

[pytest]: https://docs.pytest.org/en/latest/

### Unit tests

Aim to cover every functionality (and for sure all the critical ones) with unit
tests. Good unit tests help you and others to avoid mistakes in the future and
show by example how a piece of code is supposed to work.

Organize the tests to mirror the structure of your repo. Each test case should
only test one thing by exercising it once according to the Arrange/Act/Assert
pattern. Unit tests verify business logic quickly and deterministically so keep
them fast (<50ms ideally), use lightweight fixtures and mock I/O and external
services. Unit tests must not rely on environment variables or secrets.

Set your CI to check for coverage and fail if some sensible level is not met
(the template does this via `--cov-fail-under`).

### Functional tests

Functional tests exercise a cohesive feature or component made of several units
in a complete test environment. Use real objects where reasonable, mock only hard
external boundaries (third-party APIs, external message brokers). Examples: a data
ingestion pipeline, reading a message from a queue, processing it and writing the
result to a database, an ML pipeline composing ingestion + preprocessing + inference.

### Integration tests

Integration tests verify the interactions between your code and external systems
(databases, caches, message brokers, third-party APIs): that connections can be
established, schemas are what your system expects etc. Always reset state between
tests (setup/teardown).

### End-to-end (E2E) tests

End-to-end tests cover individual paths from user entry (UI/HTTP/CLI) to persistence
and back across the full system. They validate real user flows, deployment readiness
and infra assumptions.

### Container build / smoke tests

A smoke test is a small, fast test that checks whether the artifact we ship
actually starts and responds: build the image (proving the Dockerfile works),
run the container with a test config and assert basic behaviour (HTTP 200, a
health check...). The template CI builds the production image on every pipeline.

## Run your basic code-quality tools before committing

Using a pre-commit framework to enforce this is a good idea. We use [prek][prek],
a fast drop-in replacement for pre-commit that reads the same
`.pre-commit-config.yaml`. However it's an even better idea to run the checks
manually first, when using the template make sure all the files are added to
git and then `uv run --locked prek run --all-files`

Greatest reason for this is that some of the autoformatters etc will very
likely change your files and this will cause the commit to fail and then
you'd need to retype your commit messages (if not given via `-m`)

[prek]: https://prek.j178.dev/

## Use tox

To run your test suite across multiple python versions easily.

There is a [Docker image][toxdocker] that makes this a bit simpler, or you
could set up pyenv yourself.

[toxdocker]: https://github.com/advian-oss/docker-pyenv-tox

## Use ruff format

[Ruff][ruff] auto-formats your code to a common standard, it is a drop-in
replacement for black. Run it with `uv run --locked ruff format src tests`.

[ruff]: https://docs.astral.sh/ruff/

## Use ruff check

Ruff is also the linter, it implements the pylint rules (and plenty of others)
while being orders of magnitude faster. Keep it strict, see the minimal template
above for good default config. Run it with `uv run --locked ruff check src tests`.

## Use type hints & [pyrefly][pyrefly]

And keep it strict (the template uses the `strict` preset). Annotate every
function parameter and return value. Type hinting will make future refactoring
much safer and it will save you from a bunch of bugs right now as well. Run the
checker with `uv run --locked pyrefly check`.

### Validate at runtime where it matters

Type hints alone don't stop bad values at runtime. Always validate at the external
boundaries (HTTP, CLI, files, messages, env vars, DB rows, any place where external
data enters or leaves your system), [pydantic][pydantic] or [dataclasses][dataclasses]
with validators cover 99.9% of the cases (for the rest look at `beartype` or `typeguard`).

Keep Postel's law in mind: "be conservative in what you send, and liberal in what
you accept", i.e. produce well-formed, strict outputs but tolerate minor variations
in incoming data. For security-sensitive or safety-critical systems prefer
fail-fast behaviour over permissive acceptance.

If performance is critical, internal code can rely on static typing and tests
instead of runtime enforcement. Document which layers perform validation.

[pyrefly]: https://pyrefly.org/
[pydantic]: https://docs.pydantic.dev/latest/
[dataclasses]: https://docs.python.org/3/library/dataclasses.html

## Use pyproject.toml

This is the modern way to handle package metadata.

## Use [uv][uv]

The modern packaging and dependency management tool, it also manages the
project virtualenv and Python versions for you. Use `uv sync --locked` to
install the project (and its dev dependencies) and `uv run --locked COMMAND`
to run tools inside the project environment.

Instead of always using `uv run --locked COMMAND`, you can activate the
project virtualenv with and then run the command directly. Activation command
depends on your environment but on Linux/MacOS/etc with normal shells
it is `. .venv/bin/activate`. For other environments there are scripts under `.venv/bin/`

Always commit `uv.lock` alongside `pyproject.toml`. Run `uv lock` after editing
dependencies by hand and `uv build` to produce wheel and source distributions.

[uv]: https://docs.astral.sh/uv/

### uv pypi dependencies

`uv add packagename` (or `uv add --dev packagename` for development tools)
will add the dependency like this:

    "packagename>=1.2.3"

which only sets a lower bound, you probably want to lock the major version
so use `uv add --bounds major packagename` to get `"packagename>=1.2.3,<2.0"`
(or `--bounds minor` if the package is known to break between minor versions).

If your project does data science/machine learning, pinning to a major or even
minor version is **not enough** since transitive dependencies (which are often
poorly specified in that ecosystem) might break reproducibility of results. Add
those with `--bounds exact`, commit `uv.lock` and periodically test upgrades in CI.

### Dependency hygiene

Keep the environment minimal and clean: everything listed in `pyproject.toml`
must actually be used by the code. Production dependencies are the ones strictly
needed to run the code, everything only needed for development, testing, linting,
building or releasing (`pytest`, `ruff`, `pyrefly`, `prek`, `tox`, type stubs etc.)
goes to the `dev` dependency group via `uv add --dev`. The dev group must not be
installed in production deployments, the template's multi-stage Dockerfile takes
care of this (the production target is built from `uv export --locked --no-dev`).

Audit your dependencies for known vulnerabilities in CI (the template runs
[bandit][bandit] on the code, [pip-audit][pipaudit] checks the installed packages),
address the findings regularly and promptly remove tools you no longer use.

[bandit]: https://bandit.readthedocs.io/en/latest/
[pipaudit]: https://pypi.org/project/pip-audit/

### uv git dependencies

Make sure to use git tags for the dependencies, `uv add` puts the git source
into the `[tool.uv.sources]` table::

    uv add "git+ssh://git@github.com/pvarki/python-privatepackage" --tag 0.5.0

    [tool.uv.sources]
    privatepackage = { git = "ssh://git@github.com/pvarki/python-privatepackage", tag = "0.5.0" }

For development and testing purposes when you are developing the package you depend
to at the same time you can also use `branch = "mybranch"` but before merging your
changes to default branch make sure all git dependencies use tags (and remember to run
`uv lock` to make sure the lockfile is up-to-date)

### Weird packages

Some packages, like [PyTorch][pt] have special requirements making them complicated for
dependency management. This combined with lask of metadata API in "simple" PyPi-style
repositories means that unless great care is taken in how the dependency is specified
in `pyproject.toml` the package manager will have to download every single matching package
variant and version to inspect the embedded metadata.

`uv` has an [integration guide for PyTorch][uvpt], the principles apply to other similarly
complicated packages and other package managers that use standard PIP in the background.

[pt]: https://pytorch.org/
[uvpt]: https://github.com/astral-sh/uv/blob/main/docs/guides/integration/pytorch.md
