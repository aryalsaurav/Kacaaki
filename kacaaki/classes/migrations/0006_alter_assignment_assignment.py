# Generated by Django 4.1.6 on 2023-06-11 17:02

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0005_assignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='assignment',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FileField(upload_to='assignments/'), blank=True, size=None),
        ),
    ]
