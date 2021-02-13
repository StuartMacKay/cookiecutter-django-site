from pytest_factoryboy import register

from tests.factories.user import UserFactory

pytest_plugins = [
    "tests.fixtures",
]

register(UserFactory)
