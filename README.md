# Best practises

Coding standards etc documented.

Rendering to PDF tldr:

    docker build --progress plain --ssh default --target render -t pvarki_best_practises:render .
    docker run --rm -v `pwd`:/app pvarki_best_practises:render

## General notes

### Unified logging is important!

See [logging][logging] guidelines for details.

### No hardcoded credentials

Never hardcode usernames, passwords or other access tokens in any file
that is committed to a repository.

Use config files (remember `.gitignore` non-template configs) and/or ENV variables.

### Use UNIX newlines

In text or code, use only UNIX newlines (LF) as end-of-line. Make sure
your pre-commit hooks enforce this.

### Use UTF-8

or plain ASCII which UTF-8 is a superset of. No other encodings allowed,
it will just lead to tears.

### Don't Repeat Yourself (DRY)

aka don't copy-paste code, refactor to helper methods and libraries.

Yes, making a new library will take much longer in the short term.
It will also save a ton of work in the long term. If there's a deadline
and you absolutely positively just have to do the copy-paste at least mark
it with FIXME and create an issue to the repo about librarizing said code.

#### Continuous Integration
For any Continuous Integration (CI), make sure to add things to
[config-ci-library](https://github.com/pvarki/config-ci-library), especially
for things that are very likely reusable for other repos.

#### Creating new repositories
Likewise, when creating new repositories, make sure to use existing configs/
templates from[config-ci-library](https://github.com/pvarki/config-ci-library).
Changes to the config library are synced to template repositories, but drift is
possible with pre-commit files, for example, once the initial repo is cloned. If
there is no template for your specific use case, either use the existing configs
to manually create one, or add one following the same conventions as for existing
templates.

### Applications must be headless by default

Unless the applications main purpose is to display graphics it must
not attempt to connect to a display. In general they will be run in
docker and will not have access to a display (the host machine is also
unlikely to have one).

### Provide docker(-compose) files

This solves "works on my machine" -problems.

If your program depends on external libraries, operating system packages
or such. Or there is any other reason that there's a chance it doesn't
"just work" on any random machine someone would try to run it on: You must
provide a `Dockerfile` which creates a working environment.

If it expects to connect to a local database then you must also provide
a `docker-compose.yml` that fires up a correctly initialized database.

Remember to regularly check that your docker env also works.

## Specific notes and guidelines

  - [logging][logging] guidelines
  - [git][git] guidelines
  - [C/C++][cpp] guidelines
  - [Rust][rust] guidelines
  - [Python][python] guidelines
  - [SSH][ssh] pro tips

[ssh]: ./ssh_tips.md
[git]: ./git.md
[cpp]: ./c_and_cpp.md
[python]: ./python.md
[rust]: ./rust.md
[logging]: ./logging.md
