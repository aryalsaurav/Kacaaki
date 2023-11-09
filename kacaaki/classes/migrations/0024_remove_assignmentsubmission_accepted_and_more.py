# Generated by Django 4.1.6 on 2023-11-08 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0023_assignmentsubmission_accepted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentsubmission',
            name='accepted',
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='approval',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Submitted', 'Submitted')], default='Submitted', max_length=15),
        ),
    ]
