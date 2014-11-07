from django.contrib.auth.models import User

from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie import fields

from fit.accounts.models import UserProfile
from fit.apiauth import OAuth20Authentication
 

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        authorization = DjangoAuthorization()
        # authentication = OAuth20Authentication()
        resource_name = 'user'
 

class UserProfileResource(ModelResource):
    choices = fields.ToOneField(UserResource, 'user')

    class Meta:
        queryset = UserProfile.objects.all()
        authorization = DjangoAuthorization()
        # authentication = OAuth20Authentication()
        resource_name = 'user_profile'