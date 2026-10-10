# Rust

Remember to read the general guidelines in the main README first!

## Use cargo

Even though in theory one can use Rust compiler as-is the packaging framework
is the way to keep everyone sane.

## Start with a template

See [Advian app template][cctempl]. Use this even if you are not using Advians message
passing things, it will give bunch of other useful things that `cargo new` won't.

Most of the other stuff here is already set up correctly when using
one of Advians templates.

## Minimal dependencies

Especially if those depend on system level libraries (ie are not pure Rust)

Remember: the deployment env is never going to be identical to your
development laptop so "works on my machine" is not going to cut it.

## `cargo fmt` before commit

This enforces the "Rust style".

In fact use a pre-commit hook that makes sure this is run before committing. The
[app template][cctempl] has a good pre-commit config.

[cctempl]: https://gitlab.com/advian-oss/rust-datastreamserviceapp_template

## `cargo check` before commit

As above, have pre-commit hook enforcing this.

## Unit tests

Write them, run `cargo test` regularly (but since this might take a while maybe
not on pre-commit hook), have CI/CD run test suite automatically for PRs

## Coverage

Coverage tooling and testing To Be Defined

## Run your basic code-quality tools before committing

Using a pre-commit framework to enforce this is a good idea. However it's an
even better idea to run them manually first, when using the template make
sure all the files are added to git and then `pre-commit run --all-files`

Greatest reason for this is that some of the autoformatters etc will very
likely change your files and this will cause the commit to fail and then
you'd need to retype your commit messages (if not given via `-m`)
