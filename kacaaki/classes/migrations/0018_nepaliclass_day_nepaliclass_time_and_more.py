# Generated by Django 4.1.6 on 2023-10-31 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0017_danceassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='nepaliclass',
            name='day',
            field=models.CharField(default='h', max_length=100, verbose_name='Class Day'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nepaliclass',
            name='time',
            field=models.CharField(default='h', max_length=100, verbose_name='Class Time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='nepaliclass',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Class Name'),
        ),
    ]
