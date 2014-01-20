import factory

from ..models import User


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    email = factory.Sequence(lambda n: 'email-%s@example.com' % n)
    name = factory.Sequence(lambda n: 'User %s' % n)
