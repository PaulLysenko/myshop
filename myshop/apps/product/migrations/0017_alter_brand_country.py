# Generated by Django 4.2.7 on 2024-02-09 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_alter_product_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='country',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
    ]
