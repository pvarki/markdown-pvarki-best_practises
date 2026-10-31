# Git

Git is very powerful, this also makes it sometimes a bit complicated.

## Windows and newlines

As per [general notes](https://github.com/pvarki/markdown-pvarki-best_practises#use-unix-newlines) we
will **always** use only LF as newline, configure your git client accordingly:

```console
git config --global core.autocrlf false
git config --global core.safecrlf true
git config --global core.eol lf
```

## Use SSH for private repos

It's just better, especially with MFA (which might not work at all with
password based authentication to private repositories).

On Windows you probably need to enable the OpenSSH Authentication Agent service
since it's disabled by default, search for "services" in the box next to start menu and
open the application called "services", find the "OpenSSH Authentication Agent"
-service and doubleclick to edit it, set "Startup type" to "Automatic" and click ok.

## Default branch name

Used to be `master` is now `main` for new repos. Reasons are purely
socio-political. Editors (rambos) note: I think it should have been `trunk`
from the very beginning but I guess git wanted to be different from svn.

We are not going to change the default branch name for old repos but will use
`main` going forward, just be aware of this.

If your client used "master" as default branch for `git init` you can
change it after the first commit (before pushing to remote repo that expects
"main") with `git branch -m main`.

## Use it for any and all code

There is nothing that is too small for starting with `git-init`

## Do not `git add .` use `git commit -a`

The exception being the very first repo init.

In general be very careful when you `git add` entire directories, make
sure that each time you do they only contain files you [really want][wannabe]
in the repo. If unwanted files end up merged into the main branch (or some other
shared branch) history they're in there forever unless very drastic measures are taken.

The correct shorthand for "I want to commit all my changes" is `git commit -a`. Add
any **new** files individually with git add (or let your IDE do it when you create the file
via IDE).

See also the note about large binary files below.

[wannabe]: https://www.youtube.com/watch?v=3PqAPXpvC-4

## Learn the CLI

It's common across IDEs and other environment specific variables.

It also does exactly what you tell it to, your IDE might do it's own
magical things.

And if your pre-commit hooks (see below) fail you probably get more
useful error messages from the CLI.

There is nothing wrong with using a GUI git thing if you prefer as long
as your understand how do everything you do there also via the CLI.

## Work in a branch

**Always** work in your own branch, **never** push directly to the default branch
(`master`, `main`) or other shared branches. Use "feature branches" for development.

## Learn to `rebase -i`

When making typo-fixes etc minor commits immediately squash them to
a suitable previous commit (that has not yet been merged to a shared branch).

## Make PR/MR early

PR=Pull Request, MR=Merge Request, they are the same thing but MR is the
term used by Gitlab, many other places use PR.

Make it early so you can get early feedback from the build and test automation
of our CI pipelines.

Prefix the title with "DRAFT:" to mark this request as being still work in
progress so it won't be accidentally merged before it's done.

When you're actually done remove the DRAFT status and ask someone to review
the merge request.

Remember that small logical collections of features/fixes make for better
MRs than huge dumps of anything and everything.

## Commit early, commit often

You can (and should) clean up the history with `git rebase -i` before
marking merge-request as not DRAFT. Also `git push` often so random catastrophes
affecting your working copy do not cause major loss of work.

Smaller commits are better than large ones. Smaller commits make for
less chances of conflicts and easier resolving.

It's way easier to review code when the commits are in small sensible
chunks instead of one giant "implemented these 10 different features".

When refactoring code that was originally not up-to-spec it's acceptable to use
the SKIP env variable to skip linter checks in order to have commits of sensible size.

## push often

Not only does this allows you to have feedback from CI sooner, also if something
should happen to your local development machine/branch/repo there is a recent copy
in the cloud.

It's also much easier for others to help you when they can just pull your changes
from the cloud.

## Use fetch-rebase not fetch-merge

`git pull` does a fetch and then a merge commit, this will make your
history very messy.

Use [`git-up`][gitup] to first fetch and then rebase your branches
to their remote correspondents.

[gitup]: https://pypi.org/project/git-up/

## Rebase to main before merge

Rebase your branch to main regularly and always before marking merge-request as
not DRAFT, at this time also look at your commit log and clean it up.
[See this post for more info][rebasehowto].

[rebasehowto]: https://thoughtbot.com/blog/git-interactive-rebase-squash-amend-rewriting-history

## Use [prek][precommit]

This will make it easier to maintain high quality in your commits.

The various cookiecutter templates init the config for you but you must remember
to run `prek install` in your local checkout. To make you less likely to
forget set up [automatic enable][precommitauto] on clone.


For a minimal good configuration you can look at this repos
[`.pre-commit-config.yaml`][configyaml]

[precommit]: https://prek.j178.dev/
[configyaml]: ./.pre-commit-config.yaml
[precommitauto]: https://prek.j178.dev/#automatic-enabling-on-clone

## Use `.gitignore`

Especially make sure no real production config files are committed to the
code repositories (CI/CD deployment repos are a different story).

## Use CI

To make sure you run the test suite before merging to main.

## Use semver

[Semantic Versioning][semver], every merge to main must have unique version.

[semver]: https://semver.org/

## Tag versions when merging to main

Ideally have CI do this for you, but do it manually if you have to.

Tag format is: 1.2.3

## Large binary files

Git does not play nice with these, which is why you should always have the
`check-added-large-files` pre-commit hook enabled. Use [git-lfs][lfs] if
you really need to track binaries with the code. Otherwise consider keeping them
in some cloud storage and document how to download them.

### LFS, Azure and HTTP 413

[No-one knows why Azure is weird](https://stackoverflow.com/questions/77485593/azure-devops-git-push-fails-with-lfs-with-large-file-150mb)

```console
git config http.version HTTP/1.1
```

Solves it thuogh.

[lfs]: https://docs.gitlab.com/ee/topics/git/lfs/
