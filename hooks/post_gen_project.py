# post_gen_project.py
import os
import shutil
import subprocess

COOKIECUTTER_ENV = os.environ.get("COOKIECUTTER_ENV")

CREATE_MAKEFILE = "{{ cookiecutter.create_makefile }}" == "y"
CREATE_VIRTUALENV = "{{ cookiecutter.create_virtualenv }}" == "y"
CREATE_REPOSITORY = "{{ cookiecutter.repository_url }}" != ""

USE_PYCHARM = "{{ cookiecutter.ide }}" == "pycharm"
USE_PYTEST = "{{ cookiecutter.test_runner}}" == "pytest"
USE_READTHEDOCS = "{{ cookiecutter.use_readthedocs}}" == "y"
USE_WAGTAIL = "{{ cookiecutter.cms }}" == "wagtail"
USE_CELERY = "{{ cookiecutter.use_celery }}" == "y"

if COOKIECUTTER_ENV == 'dev':
    CREATE_VIRTUALENV = CREATE_VIRTUALENV and not os.path.exists(".venv")
    CREATE_REPOSITORY = CREATE_REPOSITORY and not os.path.exists(".git")
    USE_PYCHARM = USE_PYCHARM and not os.path.exists(".idea")


def remove(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)


def create_venv():
    python = "python{{ cookiecutter.python_version }}"
    pip = "./.venv/bin/pip{{ cookiecutter.python_version }}"
    pip_compile = "./.venv/bin/pip-compile"
    pip_sync = "./.venv/bin/pip-sync"

    subprocess.run([python, "-m", "venv", ".venv"])
    subprocess.run([pip, "install", "--upgrade", "pip", "setuptools", "wheel"])
    subprocess.run([pip, "install", "pip-tools"])

    subprocess.run([pip_compile, "requirements/dev.in", "--output-file", "requirements/dev.txt"])
    subprocess.run([pip_compile, "requirements/docs.in", "--output-file", "requirements/docs.txt"])
    subprocess.run([pip_compile, "requirements/tests.in", "--output-file", "requirements/tests.txt"])
    subprocess.run([pip_compile, "requirements/site.in", "--output-file", "requirements/site.txt"])
    subprocess.run([pip_sync, "requirements/dev.txt"])


def cleanup():
    # Delete the resources directory tree. It was only used with include
    # template directives and it not needed in the generated project.
    remove("resources")

    if not CREATE_MAKEFILE:
        remove("Makefile")

    if not USE_PYCHARM:
        remove(".idea")

    if not USE_PYTEST:
        remove("requirements/tests.in")
        remove("requirements/tests.txt")
        remove("conftest.py")
        remove("factories")
        remove("fixtures")

    if not USE_READTHEDOCS:
        remove("docs")
        remove("requirements/docs.in")
        remove("requirements/docs.txt")
        remove(".readthedocs.yml")

    if not USE_WAGTAIL:
        remove(".dockerignore")
        remove("Dockerfile")
        remove("{{ cookiecutter.site_app }}/home")
        remove("{{ cookiecutter.site_app }}/search")

    if not USE_CELERY:
        remove("{{ cookiecutter.site_app }}/celery.py")


def git_init():
    # Although there should not be any cruft in the generated project
    # leave adding and committing the files for later. That also neatly
    # sidesteps the issue of setting up or selecting the GPG key if
    # commits are going to be signed.
    subprocess.run(["git", "init"])
    subprocess.run(["git", "remote", "add", "origin", "{{ cookiecutter.repository_url }}"])


if __name__ == '__main__':

    if CREATE_VIRTUALENV:
        create_venv()

    if CREATE_REPOSITORY:
        git_init()

    cleanup()
