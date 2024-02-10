# Generated by Django 4.2.7 on 2024-01-30 10:04

import apps.product.constants
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_fileimport_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileimport',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'NEW'), (10, 'SUCCESS'), (20, 'ERROR')], default=apps.product.constants.FileImportStatus['NEW']),
        ),
    ]
