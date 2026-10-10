# Best practices

How pvarki builds software, for humans and for coding agents. Contribute with
pull requests.

## Responsibilities
Ownership: OpenDefence Head of Engineering.
- Heads and maintainers: Everything needed is here, and everything here is known.
- Each of us: everything here is followed.

## Contents

### [Rationality][rationality]: am I doing sane things?

1. You Ain't Gonna Need It (YAGNI)
2. Don't Repeat Yourself (DRY)
3. Divide and conquer
4. Validate with reality

### [General practices](#general-practices): am I doing basic things in sane ways?

1. Unified logging
2. No hardcoded credentials
3. UNIX newlines
4. UTF-8
5. Headless by default
6. Docker(-compose) files

### Tools: am I using tools in sane ways?

- [git][git], including Conventional Commits
- [CI and pre-commit][ci], with config-ci-library
- [Logging][logging]
- [Databases][databases]
- [SSH][ssh]
- [Windows 11, WSL2 and Docker][wsl11] (or [Windows 10][wsl10])

### Frameworks and languages: am I using them sanely and so that others understand my work?

- [Python][python], with an [Ubuntu setup][ubuntu]
- [TypeScript][typescript]
- [Rust][rust]
- [C/C++][cpp]

### [Agents][agents]: how coding agents work here

Installable set of rules, guidance and skills for agents to work adhering the standards.
You're welcomed to extend the Skills.

---

## General practices

### Unified logging is important!

See the [logging][logging] guidelines.

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

## Rendering to PDF

    docker build --progress plain --target render -t pvarki_best_practises:render .
    docker run --rm -v `pwd`:/app pvarki_best_practises:render

[rationality]: ./rationality/README.md
[git]: ./tools/git.md
[ci]: ./tools/ci.md
[logging]: ./tools/logging.md
[databases]: ./tools/databases.md
[ssh]: ./tools/ssh_tips.md
[wsl11]: ./tools/win11_wsl2_docker.md
[wsl10]: ./tools/win10_wsl2_docker.md
[python]: ./frameworks-languages/python.md
[ubuntu]: ./frameworks-languages/ubuntu2004_python3_setup.md
[typescript]: ./frameworks-languages/typescript.md
[rust]: ./frameworks-languages/rust.md
[cpp]: ./frameworks-languages/c_and_cpp.md
[agents]: ./agents/README.md
