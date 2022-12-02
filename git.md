# Git

Git is very powerful, this also makes it sometimes a bit complicated.


## Work in a branch

**Always** work in your own branch, **never** push directly to the default branch
(`master`, `main`) or other shared branches. Use "feature branches" for development.


## Learn to `rebase -i`

When making typo-fixes etc minor commits immediately squash them to
a suitable previous commit (that has not yet been merged to a shared branch).


## Use it for any and all code, documentation, etc

There is nothing that is too small for starting with `git init`


## Commit early, commit often

You can (and should) clean up the history with `git rebase -i` before
marking merge-request as not WIP. Also `git push` often so random catastrophes
affecting your working copy do not cause major loss of work.

Smaller commits are better than large ones. Smaller commits make for
less chances of conflicts and easier resolving.

It's way easier to review code when the commits are in small sensible
chunks instead of one giant "implemented these 10 different features".


## Use fetch-rebase not fetch-merge

`git pull` does a fetch and then a merge commit, this will make your
history very messy.

Use [`git-up`][gitup] to first fetch and then rebase your branches
to their remote correspondents.

[gitup]: https://pypi.org/project/git-up/


## Rebase to main before merge

**Rebase** (do *not* pull)  your branch to main regularly and always before marking merge-request as
not WIP, at this time also look at your commit log and clean it up.
[See this post for more info][rebasehowto].

[rebasehowto]: https://thoughtbot.com/blog/git-interactive-rebase-squash-amend-rewriting-history


## Do not squash-merge

Squash merges makes it difficult to work in multiple branches concurrently since
it always does a history rewrite leading to conflicts that have to be manually resolved.


## Default branch name

Used to be `master` is now `main` for new repos. Reasons are purely
socio-political. Editors (rambos) note: I think it should have been `trunk`
from the very beginning but I guess git wanted to be different from svn.

We are not going to change the default branch name for old repos but will use
`main` going forward, just be aware of this.

If your client used "master" as default branch for `git init` you can
change it after the first commit (before pushing to remote repo that expects
"main") with `git branch -m main`.


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


## Make PR/MR early

PR=Pull Request, MR=Merge Request, they are the same thing but MR is the
term used by Gitlab, many other places use PR.

Make it early so you can get early feedback from the build and test automation
of our CI pipelines.

Prefix the title with "WIP:" to mark this request as being still work in
progress so it won't be accidentally merged before it's done.

When you're actually done remove the WIP status and ask someone to review
the merge request.

Remember that small logical collections of features/fixes make for better
MRs than huge dumps of anything and everything.


## Use [pre-commit framework][precommit]

This will make it easier to maintain high quality in your commits.

The various cookiecutter templates init the config for you but you must remember
to run `pre-commit install` in your local checkout. To make you less likely to
forget set up [automatic enable][precommitauto] on clone.


For a minimal good configuration you can look at this repos
[`.pre-commit-config.yaml`][configyaml]

[precommit]: https://pre-commit.com/
[configyaml]: ./.pre-commit-config.yaml
[precommitauto]: https://pre-commit.com/#automatically-enabling-pre-commit-on-repositories


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

[lfs]: https://docs.gitlab.com/ee/topics/git/lfs/


## Use SSH for private repos

It's just better, especially with MFA (which might not work at all with
password based authentication to private repositories).

On Windows you probably need to enable the OpenSSH Authentication Agent service
since it's disabled by default, search for "services" in the box next to start menu and
open the application called "services", find the "OpenSSH Authentication Agent"
-service and doubleclick to edit it, set "Startup type" to "Automatic" and click ok.
