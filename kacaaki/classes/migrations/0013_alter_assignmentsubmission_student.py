# Generated by Django 4.1.6 on 2023-06-12 09:03

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('classes', '0012_alter_assignmentsubmission_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='student',
            field=models.ForeignKey(limit_choices_to=models.Q(('assignment__nepali_class', django.db.models.expressions.OuterRef('assignment__nepali_class_id'))), on_delete=django.db.models.deletion.CASCADE, to='users.nepalistudent'),
        ),
    ]
