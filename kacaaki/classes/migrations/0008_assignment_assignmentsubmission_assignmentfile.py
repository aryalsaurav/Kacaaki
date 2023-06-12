# Generated by Django 4.1.6 on 2023-06-12 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('classes', '0007_delete_assignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=250)),
                ('nepali_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.nepaliclass')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.nepalistudent')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_file', models.FileField(upload_to='assignments/')),
                ('assignment_submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.assignmentsubmission')),
            ],
        ),
    ]