from django.contrib import admin
from apps.account.models import RegTry


@admin.register(RegTry)
class RegTryAdmin(admin.ModelAdmin):
    pass
