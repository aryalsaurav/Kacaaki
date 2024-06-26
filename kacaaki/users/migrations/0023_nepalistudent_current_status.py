# Generated by Django 4.1.6 on 2024-02-20 17:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0022_alter_user_user_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="nepalistudent",
            name="current_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Enrolled", "Enrolled"),
                    ("Paused", "Paused"),
                    ("Dropped", "Dropped"),
                    ("Not Enrolled", "Not Enrolled"),
                    ("Not Interested", "Not Interested"),
                    ("Other", "Other"),
                ],
                default="Not Enrolled",
                max_length=15,
                null=True,
            ),
        ),
    ]
