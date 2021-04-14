************
Contributing
************

Making the project useful to others can keeping it up to date can be
a lot of work so contributions are welcome and appreciated. Every
contribution matters, whether it's large or small.

Report Bugs
===========

Report bugs at https://github.com/StuartMacKay/cookiecutter-django-site/issues

The hardest part is always recreating a problem so please include:

* Which operating system you are using.
* Which version of python you are using.
* Detailed steps to reproduce the bug.
* Include any snippets of code that trigger the bug.

The project is biased towards development using Linux or a similar operating
system. For example the Makefile will not work on windows and might have
subtle side-effects on other operating systems. Knowing which operating
system and version you are using can quickly identify some problems.

The project officially supports versions 3.5 onwards but likely works with
earlier versions too. It's important to know which version you are using
particularly if it is an earlier one.

Describing how to recreate a bug is the difficult part. The best way is to
write the steps down and follow them yourself. If the bug happens again you
can be pretty sure we will see the same result.

The more information you give, the faster the problem can be recreated and
a solution implemented.

Fix Bugs
========

All the known bugs will be listed in the GitHub issue. These will generally
be tagged with "bug". Anything with a "help wanted" is open to whoever wants
to implement a fix for it.

Implement Features
==================

It's a similar story with features. Look through the GitHub issues and
anything tagged with "enhancement" and "help wanted" is open to whoever
wants to implement it.

Adding integrations with third-party services is always of interest,
even if they are not listed. The cookiecutter.json file contains a couple
of choice values, for example `continuous_integration` which makes adding
new services easy. However there is a trade-off between making the project
useful and making the project comprehensive. If a service is widely used
then there's a good case for including it.

Write Documentation
===================

The process of running cookiecutter to generate a project from a template
is well documented. The README.rst for this project should be sufficient
to make the project useful. However improvements are always welcome.

The generated project itself does not have much in the way of documentation.
Where contributions would be useful is in files that take a lot of the
guesswork and some of the pain of setting up a project. Outlines for
documents are always a good idea as then it becomes easy to fill out the
details.

Submit Feedback
===============

The best way to send feedback is to file an issue at
https://github.com/StuartMacKay/cookiecutter-django-site/issues.

If you are proposing an enhancement then please explain in detail how
it would work. Please keep the scope as narrow as possible as that
makes it easier to understand and implement.

If you are just having difficulty using the project then file an issue
as that is likely an indication that something is not working the way
it was expected or the instructions need some improvements.

Get Started!
============

To set up `cookiecutter-django-site` for local development:

1. Fork the `cookiecutter-django-site` repository on GitHub.

2. Clone your fork locally::

    git clone git@github.com:<your_name>/cookiecutter-django-site.git

3. Create and activate the virtual environment::

    python3.8 -m venv venv
    pip install --upgrade pip setuptools wheel
    pip install pip-tools
    pip -r requirements/dev.txt

   Now you can activate it using::

    source venv/bin/activate

4. Create a branch for local development::

    git checkout -b <name-of-your-bugfix-or-feature>

   Now you can make your changes locally.

5. To check everything works as expected run cookiecutter::

    cookiecutter . --output-dir output

6. When you're done making changes run all the tests with tox::

    tox

7. Commit your changes and push your branch to GitHub::

    git add .
    git commit
    git push origin <name-of-your-bugfix-or-feature>

8. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests wherever possible. All the
tests for all supported versions should be passing.

2. If the pull request adds functionality, the docs should be updated.
Remember the README contains a complete description of the parameters
in cookiecutter.json.

3. Make sure you add  a note to `CHANGELOG.rst` about the changes.
Use the imperative style, see the existing entries to see how that is written.

Tips
====
To avoid having to repeatedly answer each question when running cookiecutter,
create a .cookiecutterrc file with the values you to be different from the
defaults. Here is the file that's used to generate the reference
`django-library-site` that shows how the generated project is laid out::

    # .cookiecutterrc
    #
    # The default_context contains definitions for the project specific variables
    # in cookiecutter.json.
    #

    default_context:
        project_name: "Django Library Site"
        project_description: "A Django site created by the cookiecutter-django-site template."
        project_keywords: "cookiecutter, django, site, template"
        python_version: "3.8"
        author: "Stuart MacKay"
        author_email: "smackay@flagstonesoftware.com"
        code_linter: "flake8"
        test_runner: "pytest"

Now you can run cookiecutter using the following::

    cookiecutter . --config-file .cookiecutterrc --no-input --output-dir output

To avoid generating the virtualenv on each run and installing all the requirements
set the following environment variable::

    export COOKIECUTTER_ENV=dev

To avoid having to delete the generated output everytime use the
``--overwrite-if-exists`` flag::

    cookiecutter . --config-file .cookiecutterrc --no-input --overwrite-if-exits --output-dir output

