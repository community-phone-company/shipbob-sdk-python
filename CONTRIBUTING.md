# Contributing Guide

Welcome! This is part of the set of open source projects that are
being developed at Community Phone. These projects are meant to be
shared and developed in collaboration with anyone, individuals and
other companies alike. This is a quick set of guidelines to contribute
to any of our Open Source Projects.

### Creating an issue

If you experience any problem while using this software or want to request a feature
then you should open an issue against the repository. All issues should
contain:

**For Feature Requests:**

- A description of the feature you would like to see implemented
- An explanation of the value that such a feature would provide for you *and others*.
- A brief explanation of why this should be done on this project (instead of any other existing system)


**For Bugs:**

- A short description of the problem
- As relevant as possible description of your system (Operating System, python version, etc)
- What was the exact unexpected thing that occured.
- What you were expecting to happen instead.

### Creating a PR (Pull Request)

If you are a software developer and would like to contribute to this
project, you can open a Pull Request(PR) against the repository.

All PRs should be:

- Self-contained.
- As short as possible and address a single issue or even a part of an issue.
  Consider breaking long PRs into smaller ones.

In order for a Pull Request to get merged into the main repository you should
have one approved review from one of the Community Phone developers.
Continuous Integration tests should be passing and the CI build should be
green.

Additionally you need to sign the project CLA (Contributor License
Agreement). Our CLA bot will help you with that after you created a pull
request. If you or your employer do not hold the whole copyright of the
authorship submitted we can not accept your contribution.

When you make a PR that's not ready for a review, open a Draft PR. To
open a Draft PR, find a small triangle on the green button. Otherwise,
if you open a non-Draft PR, a reviewer will be automatically assigned
to your PR.

### Pull Request Reviews

It is the responsibility of the author to ask for at least one person
to review their Pull Request. That person should know the area of the
code being changed.

PR authors should make pull request reviews easier. Make them as small
as possible and even if some code is touched it does not mean that it
needs to be refactored. For example don't mix style/typing changes
with a big PR.


### Commiting Rules

For an exhaustive guide read [this](http://chris.beams.io/posts/git-commit/)
guide. It's all really good advice. Some rules that you should always follow though are:

- A commit title not exceeding 50 characters
- A blank line after the title (optional if there is no description)
- A description of what the commit did (optional if the commit is really small)

Why are these rules important? All tools that consume git repos and show you
information treat the first 80 characters as a title. Even Github itself does
this. And the git history looks really nice and neat if these simple rules are
followed.


### Coding Style

All code should be formatted in a way that passes the check from
`black` and `flake8` according the configuration available on
`pyproject.toml`. The project follows PEP8 as closely as possible,
only deviating from it that we accept a 99-character limit.
