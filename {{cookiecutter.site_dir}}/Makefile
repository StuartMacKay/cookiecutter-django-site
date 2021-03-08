#
# Makefile: Commands to simplify development and releases
#
# Usage:
#
#    make clean
#    make checks
#    make test-all
#    make patch

# You can set these variable on the command line.
PYTHON = python{{ cookiecutter.python_version }}

# Where everything lives
site_python := /usr/bin/env $(PYTHON)

root_dir := $(realpath .)
venv_dir = $(root_dir)/.venv
site_dir = $(root_dir)/{{ cookiecutter.site_app }}

python = $(venv_dir)/bin/python3
pip = $(venv_dir)/bin/pip3
pip-compile = $(venv_dir)/bin/pip-compile
pip-sync = $(venv_dir)/bin/pip-sync
django = $(python) $(root_dir)/manage.py
{%- if cookiecutter.code_checker in ["flake8", "pylama"] %}
checker = $(venv_dir)/bin/{{ cookiecutter.code_checker }}
{%- endif %}
{%- if cookiecutter.use_black == "y" %}
black = $(venv_dir)/bin/black
{%- endif %}
{%- if cookiecutter.use_isort == "y" %}
isort = $(venv_dir)/bin/isort
{%- endif %}
{%- if cookiecutter.test_runner == "pytest" %}
pytest = $(venv_dir)/bin/pytest
{%- endif %}
{%- if cookiecutter.use_coverage == "y" %}
coverage = $(venv_dir)/bin/coverage
{%- endif %}
{%- if cookiecutter.use_bumpversion == "y" %}
bumpversion = $(venv_dir)/bin/bump2version
{%- endif %}
tox = $(venv_dir)/bin/tox
twine = $(venv_dir)/bin/twine


commit_opts :={% if cookiecutter.sign_commits %} --gpg-sign{% endif %}
{%- if cookiecutter.test_runner == "pytest" %}
{%- set opts = [] %}
{%- if cookiecutter.code_checker == "flake8" %}{{ opts.append("--flake8") or "" }}{% endif %}
{%- if cookiecutter.code_checker == "pylama" %}{{ opts.append("--pylama") or "" }}{% endif %}
{%- if cookiecutter.use_black == "y" %}{{ opts.append("--black") or "" }}{% endif %}
{%- if cookiecutter.use_isort == "y" %}{{ opts.append("--isort") or "" }}{% endif %}
pytest_opts := {{ opts|join(" ")}}
{%- endif %}

# include any local makefiles
-include *.mk

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  help                 to show this list"
{%- if cookiecutter.use_readthedocs == "y" %}
	@echo "  clean-docs           to clean the generated HTML documentation"
{%- endif %}
	@echo "  clean-tests          to clean the directories created during testing"
{%- if cookiecutter.use_coverage == "y" %}
	@echo "  clean-coverage       to clean the test coverage data and reports"
{%- endif %}
	@echo "  clean-venv           to clean the virtualenv"
	@echo "  clean                to clean everything EXCEPT the virtualenv"
	@echo
	@echo "  checks               to run quality code checks"
{%- if cookiecutter.use_coverage == "y" %}
	@echo "  coverage             to measure the test coverage"
{%- endif %}
{%- if cookiecutter.use_readthedocs == "y" %}
	@echo "  docs                 to build the HTML documentation"
{%- endif %}
	@echo "  install              to install or update the dependencies in the virtualenv"
{%- if cookiecutter.use_bumpversion == "y" %}
	@echo "  major                to update the version number for a major release, e.g. 2.1 to 3.0"
{%- endif %}
	@echo "  messages             to run the makemessages and compilemessages management commands"
	@echo "  migrate              to run the migrate management command"
	@echo "  migrations           to run the makemigrations management command"
{%- if cookiecutter.use_bumpversion == "y" %}
	@echo "  minor                to update the version number for a minor release, e.g. 2.1 to 2.2"
	@echo "  patch                to update the version number for a patch release, e.g. 2.1.1 to 2.1.2"
{%- endif %}
	@echo "  runserver            to run the runserver management command"
	@echo "  test                 to run the tests during development"
	@echo "  test-all             to run the tests for all the supported environments"
	@echo "  venv                 to create the virtualenv"
	@echo
{%- if cookiecutter.use_readthedocs == "y" %}

.PHONY: clean-docs
clean-docs:
	cd docs && make clean
{%- endif %}

.PHONY: clean-tests
clean-tests:
	rm -rf .tox
{%- if cookiecutter.test_runner == "pytest" %}
	rm -rf .pytest_cache
{%- endif %}
{%- if cookiecutter.use_coverage == "y" %}

.PHONY: clean-coverage
clean-coverage:
	rm -rf .coverage
	rm -rf reports/coverage
{%- endif %}

.PHONY: clean-venv
clean-venv:
	rm -rf $(venv_dir)

.PHONY: clean
clean: clean-tests clean-coverage{% if cookiecutter.use_readthedocs == "y" %} clean-docs{% endif %}

$(pip):
	$(pip) install --upgrade pip setuptools wheel

$(pip-compile): $(pip)
	$(pip) install pip-tools

.PHONY: checks
checks:
	$(checker) $(site_dir)
	{%- if cookiecutter.use_black %}
	$(black) --check $(site_dir)
	{%- endif %}
	{%- if cookiecutter.use_isort %}
	$(isort) --check $(site_dir)
	{%- endif %}

{% if cookiecutter.use_coverage == "y" -%}
.PHONY: coverage
coverage:
    {%- if cookiecutter.test_runner == "django" %}
	$(coverage) run --rcfile=setup.cfg manage.py test {{ cookiecutter.site_app }}
	$(coverage) html --rcfile=setup.cfg
	{%- else %}
	$(pytest) --cov={{ cookiecutter.site_app }} --cov-config=setup.cfg --cov-report html
	{%- endif %}
{%- endif %}

{% if cookiecutter.use_readthedocs == "y" -%}
.PHONY: docs
docs:
	cd docs && make html
{%- endif %}

.PHONY: install
install: venv $(pip-compile) requirements
	$(pip-sync) requirements/dev.txt

.PHONY: major
major:
	$(bumpversion) major

.PHONY: messages
messages:
	$(django) makemessages --no-obsolete --all && $(django) compilemessages --ignore .venv

.PHONY: migrate
migrate:
	$(django) migrate

.PHONY: migrations
migrations:
	$(django) makemigrations

.PHONY: minor
minor:
	$(bumpversion) minor

.PHONY: patch
patch:
	$(bumpversion) patch

requirements/dev.txt: requirements/*.in
	$(pip-compile) requirements/dev.in

requirements/docs.txt: requirements/docs.in
	$(pip-compile) requirements/docs.in

requirements/tests.txt: requirements/tests.in
	$(pip-compile) requirements/tests.in

requirements: requirements/*.txt

.PHONY: runserver
runserver: venv
	$(django) migrate
	$(django) runserver

.PHONY: test
test:
{%- if cookiecutter.test_runner == "django" %}
	$(django) test {{ cookiecutter.site_app }}
{%- else %}
	$(pytest) $(pytest_opts)
{%- endif %}

.PHONY: test-all
test-all: test
	$(tox)
	{% if cookiecutter.use_readthedocs == "y" %}tox -e docs{% endif %}

$(venv_dir):
	$(site_python) -m venv $(venv_dir)

.PHONY: venv
venv: $(venv_dir)
