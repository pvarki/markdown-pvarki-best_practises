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
