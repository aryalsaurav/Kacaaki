# Generated by Django 4.1.6 on 2023-04-29 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_rename_is_dance_student_dancestudent_is_dance_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nepalistudent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='nepali_student', to=settings.AUTH_USER_MODEL),
        ),
    ]