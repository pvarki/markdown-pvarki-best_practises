# C/C++

## Don't use C (use Rust)

C-libraries are simple to bind to Rust. There are plenty of
examples of how to do this in a good way.

For C++ libraries that do not have a C API as well things
get complicated and you might have to use native C++.

## One command builds

Make sure there's a target in your Dockerfile that provides an installable
package, especially if the program for some reason cannot be run under Docker
(if it has some weird license management thing like Sightcorp)

## Enable all warnings

Enable all compiler warnings: `-Wall -Wextra -Wshadow -Wnon-virtual-dtor -pedantic`

Clean up you code so that you don't get a ton of warnings when compiling.

## Use pre-commit template

Good template To Be Made, but autoformatter ([clang-format][cformat]) and
linter with the minimal config in this repo at least.

## Coding style

[Google coding style][gstyle]

Use [clang-format][cformat] with `BasedOnStyle: Google` in `.clang-format` file.

[gstyle]: https://google.github.io/styleguide/cppguide.html
[cformat]: https://clang.llvm.org/docs/ClangFormat.html

## Unit testing framework

[Google Test][googletest]

[googletest]: https://github.com/google/googletest

## Use Bazel (or CMake) for building

Google Test recommends [Bazel][bazel] but also supports CMake.

[bazel]: https://docs.bazel.build/versions/3.4.0/tutorial/cpp.html

## Linter

Use [cpplint][cpplint] (it's designed by Google for Google style).

[cpplint]: https://pypi.org/project/cpplint/
