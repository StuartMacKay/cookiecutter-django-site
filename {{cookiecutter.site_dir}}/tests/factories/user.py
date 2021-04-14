from django.contrib.auth import models

import factory
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):

    username = fake.user_name()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()

    class Meta:
        model = models.User
