import pytest


@pytest.fixture
def create_user(db, django_user_model, faker):
    def make_user(**kwargs):
        if "password" not in kwargs:
            kwargs["password"] = faker.password()
        if "username" not in kwargs:
            kwargs["username"] = faker.user_name()
        return django_user_model.objects.create_user(**kwargs), kwargs["password"]

    return make_user


@pytest.fixture
def user_client(db, client, create_user):
    def make_user_client(user=None):
        if user is None:
            user, password = create_user()
            client.login(username=user.username, password=password)
        else:
            client.force_login(user)
        return user, client

    return make_user_client
