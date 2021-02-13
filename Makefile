#
# Makefile: Commands to simplify development and releases
#
# Cookiecutter:
# To avoid having to enter values for all the configuration options each
# time, the cookiecutter command is run the --config-file and --no-input
# options. --no-input just accepts all the defaults from cookiecutter.json.
# These are selectively overridden by the default context in .cookiecutterrc,
# located in the root of the project, with project specific details.
#
# Variable assignment:
# Most variable assignments use '=' (recursively expanded) so they can be
# overridden by redefining them in any included makefile.
#
# Virtualenv management:
# The makefile assumes a virtualenv is created locally using python's venv
# module. However you are not limited to this option. If you use direnv,
# pyenv etc. you can define the location of the virtualenv by overriding the
# venv_dir variable in an included makefile. For example:
#
#    # env.mk
#    venv_dir = $(root_dir)/.direnv/python-3.8.6
#
# that avoids having to makes changes here and deal with keeping them out of
# the repository.

# You can set these variable on the command line.
PYTHON = python3.8

# Where everything lives
site_python := /usr/bin/env $(PYTHON)

root_dir := $(realpath .)
venv_dir = $(root_dir)/.venv
output_dir = $(root_dir)/output

python = $(venv_dir)/bin/python3
pip = $(venv_dir)/bin/pip3
pip-compile = $(venv_dir)/bin/pip-compile
pip-sync = $(venv_dir)/bin/pip-sync
pytest = $(venv_dir)/bin/pytest
tox = $(venv_dir)/bin/tox
bumpversion = $(venv_dir)/bin/bump2version
cookiecutter = $(venv_dir)/bin/cookiecutter

# include any local makefiles.
-include *.mk

.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo ""
	@echo "  clean-output       to clean the output directory"
	@echo "  clean-tests        to clean the directories created during testing"
	@echo "  clean-venv         to clean the virtualenv"
	@echo "  bake               to run cookiecutter and generate the project"
	@echo "  install            to install the dependencies"
	@echo "  major              to update the version number for a major release, e.g. 2.1 to 3.0"
	@echo "  minor              to update the version number for a minor release, e.g. 2.1 to 2.2"
	@echo "  patch              to update the version number for a patch release, e.g. 2.1.1 to 2.1.2"
	@echo "  test               to run the tests for all the supported environments"
	@echo "  venv               to create the virtualenv"
	@echo

.PHONY: clean-output
clean-output:
	rm -rf $(output_dir)

.PHONY: clean-tests
clean-tests:
	rm -rf .tox
	rm -rf .pytest_cache

.PHONY: clean-venv
clean-venv:
	rm -rf $(venv_dir)

.PHONY: bake
bake:
	$(cookiecutter) . \
	    --config-file .cookiecutterrc \
	    --overwrite-if-exists \
	    --no-input \
	    --output-dir $(output_dir)

.PHONY: install
install:
	$(pip) install --upgrade pip setuptools wheel
	$(pip) install pip-tools
	$(pip-sync) requirements/dev.txt

.PHONY: major
major:
	$(bumpversion) major

.PHONY: minor
minor:
	$(bumpversion) minor

.PHONY: patch
patch:
	$(bumpversion) patch

.PHONY: test
test:
	$(tox)

.PHONY: venv
venv:
	$(site_python) -m venv $(venv_dir)
