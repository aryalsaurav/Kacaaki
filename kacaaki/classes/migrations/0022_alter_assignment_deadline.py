# Generated by Django 4.1.6 on 2023-11-02 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0021_assignment_created_at_assignment_deadline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
