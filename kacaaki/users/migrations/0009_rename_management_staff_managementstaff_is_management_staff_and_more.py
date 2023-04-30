# Generated by Django 4.1.6 on 2023-04-28 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_token_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='managementstaff',
            old_name='management_staff',
            new_name='is_management_staff',
        ),
        migrations.AddField(
            model_name='dancestudent',
            name='is_Dance_student',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='nepalistudent',
            name='is_nepali_student',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='is_teacher',
            field=models.BooleanField(default=True),
        ),
    ]
