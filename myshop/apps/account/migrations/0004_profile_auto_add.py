from django.db import migrations
from django.contrib.auth.models import User
from apps.account.models import Profile


def to_appy(apps, schema_editor):
    try:
        users = User.objects.filter(profile__isnull=True)
        for user in users:
            Profile.objects.create(user=user)
    except Exception as e:
        print('Unavailable to run migration')


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile'),
    ]

    operations = [
        migrations.RunPython(to_appy)
    ]
