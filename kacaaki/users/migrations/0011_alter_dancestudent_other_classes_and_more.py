# Generated by Django 4.1.6 on 2023-10-11 16:50

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_nepalistudent_class_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dancestudent',
            name='other_classes',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Nepali Classes', 'Nepali Classes'), ('Music Classes', 'Music Classes')], max_length=50),
        ),
        migrations.AlterField(
            model_name='nepalistudent',
            name='other_classes',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Dance Classes', 'Dance Classes'), ('Music Classes', 'Music Classes')], max_length=50),
        ),
    ]
