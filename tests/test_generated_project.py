import os
import subprocess

import pytest

CONTEXT = {
    "test_runner": "pytest",
    "use_celery": "n",
}

env = os.environ.copy()
env["ENV"] = "dev"
env["ALLOWED_HOSTS"] = "localhost"
env["DEBUG"] = "false"
env["DEFAULT_FROM_EMAIL"] = "noreply@example.com"
env["DJANGO_SECRET_KEY"] = "secret"
env["DJANGO_SITE_ID"] = "1"
env["LOG_FORMATTER"] = "console"
env["LOG_LEVEL"] = "ERROR"
env["SENTRY_ENABLED"] = "false"


# None of the calls to subprocess.run() pass capture_output=True. There
# is no need if the test is passing and it's easily added if the test
# is failing. Alternatively when running pytest from the command line
# you can pass in --keep-baked-projects to stop any clean up after the
# tests have run. You can then find the generated project in /tmp and
# run the command directly to see why it's failing.


@pytest.fixture(scope="session")
def project(cookies_session):
    """Generate the project and return the path to the root directory

    The session scoped cookies fixture is not documented. It was added in
    https://github.com/hackebrot/pytest-cookies/pull/46/
    """
    result = cookies_session.bake(extra_context=CONTEXT)
    return str(result.project)


def test_run_migrations(project):
    """Verify the migrations run so we know Django is configured correctly"""
    python = os.path.join(project, ".venv", "bin", "python")
    db = os.path.join(project, "db.sqlite3")
    assert not os.path.exists(db)
    subprocess.run([python, "manage.py", "migrate"], cwd=project, check=True, env=env)
    assert os.path.exists(db)


def test_run_tests(project):
    """Verify the tests run successfully, including black, flake8 and isort checks"""
    runner = os.path.join(project, ".venv", "bin", "pytest")
    subprocess.run([runner, "tests"], cwd=project, check=True, env=env)

