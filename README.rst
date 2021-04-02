************************
cookiecutter-django-site
************************

A Cookiecutter_ template that contains everything you need to develop a
Django site. The template lays out the project, adds tools to support
development and testing and configures the site with essential infrastructure.

The template generates a complete working site right out of the box. All
the features are optional so you get what you need and none of the things
you didn't want.

Features
========

* Generate a working Django site right of the box.
* Code checking with `flake8`_ or `pylama`_.
* Code formatting with `black`_ and `isort`_.
* Automatically add project configuration to `PyCharm`_.
* Automatically activate the virtualenv with `direnv`_.
* Manage package versions and the virtualenv with `pip-tools`_.
* Manage repetitive project tasks with `make`_.
* Configure the site to use a CMS such as `Wagtail`_
* Configure the site to run background and periodic tasks with `Celery`_.
* Configure the site to log errors with `Sentry`_.
* Configure the site to log structured data with `structlog`_ and `django-structlog`_.
* Colour output written to the console with `colorama`_
* Run tests for all supported environments using `tox`_.
* Publish documentation to `Read the Docs`_.
* Profile and debug requests using `django-debug-toolbar`_.

Quick start
===========

Ensure you have cookiecutter installed::

    pip install --user cookiecutter

Change to the directory where the project will be generated::

    cd ~/Development

Then use cookiecutter to generate your project from this template with::

    cookiecutter gh:StuartMacKay/cookiecutter-django-site

Answer all the configuration options and you are good to go::

    cd <my new site>
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver


Configuration options
=====================

To generate the project you will be asked for the following fields, in order:

.. list-table::
    :header-rows: 1

    * - Field
      - Default
      - Description

    * - site_name
      - Django MySite
      - The project's official or human-readable name.

    * - site_dir
      - django-mysite
      - This is the name for the project's root directory. Generally this is also
        the name of the project for the repository.

    * - site_app
      - project
      - The name of the Django app that contains the settings etc. "project" is used
        as there is no real need to use a project specific name as it's not imported
        anywhere.

    * - repository_url
      - <blank>
      - The URL used to checkout the code, for example:
        git@github.com:StuartMacKay/cookiecutter-django-site.git. Leave
        blank if you do not want to set up the repository right away.

    * - python_version
      - 3.8
      - The version of the python interpreter to use. This is used in the
        Makefile when creating the virtualenv for the project.

    * - author
      - Author's full name
      - Main author of this site. This can also be the name of an organisation.

    * - author_email
      - Author's email address
      - The email address of the main point of contact for the project. This
        is also used as the point of contact in licenses and copyright notices.

    * - create_makefile
      - y
      - Add a (GNU Make) Makefile to automate project tasks.

    * - create_virtualenv
      - y
      - Create the virtualenv and install the requirements when the project
        is generated.

    * - ide
      - pycharm
      - Create the configuration files for an Integrated Development Environment.
        The list of choices includes:

        * `pycharm`_
        * other

    * - code_checker
      - flake8
      - Tools for checking code quality. The list of choices includes:

        * `flake8`_
        * `pylama`_
        * other

    * - use_black
      - y
      - Use black for formatting the source files in project.

    * - use_isort
      - y
      - Use isort for organising the import statements in your source files.

    * - use_readthedocs
      - y
      - Generate project documentation, using Sphinx, that can be hosted on
        `Read The Docs`_.

    * - use_coverage
      - y
      - Check the quality of your tests using coverage.

    * - sphinx_theme
      - sphinx-rtd-theme
      - The theme to use when generating the docs for Read the Docs. The list
        of choices includes:

        * sphinx-rtd-theme
        * alabaster
        * other

        The theme is only used if ``use_readthedocs`` is set.

    * - test_runner
      - django
      - The test runner to use. Available options include:

        * django
        * `pytest`_

        Nose has been on maintenance since 2015 so it is not included here.
        There does seem to be a follow-up project, nose2, but it's not clear
        how much life it has right now.

    * - cms
      - none
      - Install a django-based content management system.
        Available options include:

        * none
        * `wagtail`_

    * - use_celery
      - y
      - Use `Celery`_ for running and scheduling tasks in the background.

    * - use_debug_toolbar
      - y
      - Use `django-debug-toolbar`_ for displaying debug information
        the current request/response.

    * - use_sentry
      - y
      - Use `Sentry`_ for logging errors on staging and production.

    * - use_structlog
      - y
      - Use `structlog`_ and `django-structlog`_ for logging structured data
        on staging and production. Console output is prettified with `colorama`_.


Changelog
=========

See the `CHANGELOG.rst`_ for a complete history of changes and what is currently
being prepared for release.

Roadmap
=======

See the `ROADMAP.rst`_ for details on what's coming.

.. _black: https://black.readthedocs.io/en/stable/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _CHANGELOG.rst: https://github.com/StuartMacKay/cookiecutter-django-site/blob/master/CHANGELOG.rst
.. _Celery: https://docs.celeryproject.org/en/stable/index.html
.. _colorama: https://github.com/tartley/colorama
.. _direnv: https://direnv.net/
.. _django-celery-beat: https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html#beat-custom-schedulers
.. _django-debug-toolbar: https://github.com/jazzband/django-debug-toolbar
.. _django-structlog: https://github.com/jrobichaud/django-structlog
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://pycqa.github.io/isort/
.. _make: https://www.gnu.org/software/make/manual/html_node/index.html
.. _PEP 0314: https://www.python.org/dev/peps/pep-0314/
.. _pip-tools: https://github.com/jazzband/pip-tools
.. _PyCharm: https://www.jetbrains.com/pycharm/
.. _pylama: https://pylama.readthedocs.io/en/latest/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Read the Docs: https://readthedocs.org/
.. _ROADMAP.rst: https://github.com/StuartMacKay/cookiecutter-django-site/blob/master/ROADMAP.rst
.. _Sentry: https://sentry.io/
.. _Signing Your Work: https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work
.. _structlog: https://www.structlog.org/en/stable/
.. _tox: https://tox.readthedocs.io/en/latest/
.. _wagtail: https://wagtail.io/
