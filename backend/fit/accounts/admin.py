from django.contrib import admin

from fit.accounts.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)