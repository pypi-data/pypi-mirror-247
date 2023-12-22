# db-contrib-tool

The `db-contrib-tool` - MongoDB's tools for contributors.

## Table of contents

- [db-contrib-tool](#db-contrib-tool)
  - [Table of contents](#table-of-contents)
  - [Description](#description)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributor's Guide (local development)](#contributors-guide-local-development)
    - [Install project dependencies](#install-project-dependencies)
    - [Run command line tool (local development)](#run-command-line-tool-local-development)
    - [Run linters](#run-linters)
    - [Run tests](#run-tests)
    - [Pre-commit](#pre-commit)
    - [Testing changes in mongo](#testing-changes-in-mongo)
    - [Test pipx package](#test-pipx-package)
    - [Versioning](#versioning)
    - [Code Review](#code-review)
    - [Deployment](#deployment)

## Description

The command line tool with various subcommands:
- `bisect` - performs an evergreen-aware git-bisect to find the 'last passing version' and 'first failing version' of mongo
- `setup-repro-env`
  - [README.md](https://github.com/10gen/db-contrib-tool/blob/main/src/db_contrib_tool/setup_repro_env/README.md)
  - downloads and installs:
    - particular MongoDB versions
    - debug symbols
    - artifacts (including resmoke, python scripts etc)
    - python venv for resmoke, python scripts etc
- `symbolize`
  - [README.md](https://github.com/10gen/db-contrib-tool/blob/main/src/db_contrib_tool/symbolizer/README.md)
  - Symbolizes stacktraces from recent `mongod` and `mongos` binaries compiled in Evergreen, including patch builds, mainline builds, and release/production builds.
  - Requires authenticating to an internal MongoDB symbol mapping service.

## Dependencies

- Python 3.9 or later (python3 from the [MongoDB Toolchain](https://github.com/10gen/toolchain-builder/blob/master/INSTALL.md) is highly recommended)

## Installation

Make sure [dependencies](#dependencies) are installed.
Use [pipx](https://pypa.github.io/pipx/) to install db-contrib-tool that will be available globally on your machine:
```bash
$ python3 -m pip install pipx
$ python3 -m pipx ensurepath
```

Installing db-contrib-tool:
```bash
$ python3 -m pipx install db-contrib-tool
```

Upgrading db-contrib-tool:
```bash
$ python3 -m pipx upgrade db-contrib-tool
```

## Usage

Print out help message:
```bash
$ db-contrib-tool -h
```
More information on the usage of `setup-repro-env` can be found [here](https://github.com/10gen/db-contrib-tool/blob/main/src/db_contrib_tool/setup_repro_env/README.md).

## Contributor's Guide (local development)

### Install project dependencies

This project uses [poetry](https://python-poetry.org/) for dependency management.
```bash
$ poetry install
```

### Run command line tool (local development)

```bash
$ ENV=DEV poetry run db-contrib-tool -h
```

### Run linters

```bash
$ poetry run isort src tests
$ poetry run black src tests
```

### Run tests

```bash
$ poetry run pytest
```

### Pre-commit

This project has [pre-commit](https://pre-commit.com/) configured. Pre-commit will run
configured checks at git commit time.<br>
To enable pre-commit on your local repository run:
```bash
$ poetry run pre-commit install
```

To run pre-commit manually:
```bash
$ poetry run pre-commit run
```

### Testing changes in mongo

This tool is used to help run tests in the mongodb/mongo repository. On occasion, it may be
desirable to run a mongodb-mongo-* patch build with in-flight changes to this repository. The
following steps can be take to accomplish that.

- Create a branch with the changes you wish to test.
- Push the branch to the origin repository: `git push -u origin <branch_name>`.
- In the "mongo" repository, edit the [evergreen/prelude_db_contrib_tool.sh](https://github.com/10gen/mongo/blob/b1a3a357af735a53981737d91fd49e5e3ae67b95/evergreen/prelude_db_contrib_tool.sh#L10)
  to install from the git repository instead of from pypi:

  ```bash
  pipx install "git+ssh://git@github.com/<user_name>/db-contrib-tool.git@<branch_name>" || exit 1
  ```

- Create a patch build.

The patch build should now pull down the changes from your branch instead of using the published
db-contrib-tool.

**Note**: Since the db-contrib-tool is pulled from your branch, if you need to make additional
changes to the tool, you can just push to the branch and then restart the desired tasks. There is
no need to create an additional patch build unless you also need to make updates to the mongo
repository.

### Test pipx package

Pipx installation recommendations can be found in [installation](#installation) section.<br>
The tool can be installed via pipx from your local repo:
```bash
$ python3 -m pipx install /path/to/db-contrib-tool
```

### Versioning

This project uses [semver](https://semver.org/) for versioning.
Please include a description what is added for each new version in `CHANGELOG.md`.

### Code Review

Please open a Github Pull Request for code review.
This project uses the [Evergreen Commit Queue](https://github.com/evergreen-ci/evergreen/wiki/Commit-Queue#pr).
Add a PR comment with `evergreen merge` to trigger a merge.

### Deployment

Deployment to pypi is automatically triggered on merges to main.
