# Generated by Django 4.1.6 on 2023-11-02 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0019_alter_nepaliclass_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='danceclass',
            name='class_type',
            field=models.CharField(choices=[('Group Class', 'Group Class'), ('One-One Class', 'One-One Class')], default='Group Class', max_length=100, verbose_name='Class Type'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='danceclass',
            name='day',
            field=models.CharField(choices=[('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], default='Monday', max_length=100, verbose_name='Class Day'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='danceclass',
            name='time',
            field=models.CharField(default='7:30', max_length=100, verbose_name='Class Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nepaliclass',
            name='class_type',
            field=models.CharField(choices=[('Group Class', 'Group Class'), ('One-One Class', 'One-One Class')], default='Group Class', max_length=100, verbose_name='Class Type'),
            preserve_default=False,
        ),
    ]
