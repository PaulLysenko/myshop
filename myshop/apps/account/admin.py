from django.contrib import admin
from django.urls import re_path

from apps.account.models import RegTry, UserTwoFactorAuthData
from apps.account.views import SetupTwoFactorAuthView


@admin.register(RegTry)
class RegTryAdmin(admin.ModelAdmin):
    # list_display = ['id', 'email']
    pass


@admin.register(UserTwoFactorAuthData)
class UserTwoFactorAuthDataAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        urls.append(
            re_path(
                r'setup-gauth',
                self.admin_site.admin_view(SetupTwoFactorAuthView.as_view()),
                name='setup-gauth',
            ),
        )

        return urls
