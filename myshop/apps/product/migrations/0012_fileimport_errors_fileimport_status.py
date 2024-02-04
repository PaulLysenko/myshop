# Generated by Django 4.2.7 on 2024-01-26 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_fileimport_quantity_new_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileimport',
            name='errors',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fileimport',
            name='status',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]