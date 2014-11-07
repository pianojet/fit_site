from datetime import timedelta, datetime, date, time
import factory

from django.contrib.auth.models import User

from fit.accounts.models import UserProfile


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: "username%s" % n)
    first_name = factory.Sequence(lambda n: "first_name%s" % n)
    last_name = factory.Sequence(lambda n: "last_name%s" % n)
    email = factory.Sequence(lambda n: "email%s@example.com" % n)
    is_staff = False
    is_active = True
    is_superuser = False
    user_profile = factory.RelatedFactory('fit.accounts.factories.UserProfileFactory', factory_related_name='user')


class UserProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UserProfile

    user = factory.SubFactory(UserFactory, user_profile=None)
    birthdate = date(year=2000, month=1, day=1)
    

class AdminUserProfileFactory(UserProfileFactory):
    user__is_staff = True
    user__is_superuser = True