# Generated by Django 4.1.6 on 2023-06-07 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('full_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('age', models.IntegerField(null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('key', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='Key')),
                ('expiration_date', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_type', models.CharField(choices=[('Nepali Teacher', 'Nepali Teacher'), ('Dance Teacher', 'Dance Teacher')], max_length=20)),
                ('zoom_link', models.URLField(max_length=250)),
                ('is_teacher', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NepaliStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signing_for', models.CharField(max_length=20)),
                ('parents_name', models.CharField(max_length=50)),
                ('nepali_at_home', models.CharField(choices=[('Always', 'Always'), ('Sometimes', 'Sometimes'), ('Never', 'Never')], max_length=15)),
                ('listening', models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('speaking', models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('reading', models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('writing', models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('course_level', models.CharField(choices=[('L0', 'Get comfortable before learnign alphabets'), ('L1 White', 'Learn Alphabets'), ('L2 Orange', 'Learn Alphabets and words'), ('L3 Blue', 'Learn Alphabets, words and sentences'), ('L4 Yellow', 'Learn Alphabets, words, sentences and reading')], max_length=20)),
                ('session_type', models.CharField(choices=[('Group Class 1 seesion per week', 'Group Class 1 session per week'), ('Group Class 2 seesion per week', 'Group Class 2 session per week'), ('One-One class 1 session per week', 'One-One class 1 session per week'), ('One-One class 2 session per week', 'One-One class 2 session per week')], max_length=32)),
                ('class_time', multiselectfield.db.fields.MultiSelectField(choices=[('Sunday Morning', 'Sunday Morning'), ('Sunday Evening', 'Sunday Evening'), ('Monday Morning', 'Monday Morning'), ('Monday Evening', 'Monday Evening'), ('Tuesday Morning', 'Tuesday Morning'), ('Tuesday Evening', 'Tuesday Evening'), ('Wednesday Morning', 'Wednesday Morning'), ('Wednesday Evening', 'Wednesday Evening'), ('Thursday Morning', 'Thursday Morning'), ('Thursday Evening', 'Thursday Evening'), ('Friday Morning', 'Friday Morning'), ('Friday Evening', 'Friday Evening'), ('Saturday Morning', 'Saturday Morning'), ('Saturday Evening', 'Saturday Evening')], max_length=100)),
                ('goal_for_class', models.TextField(null=True)),
                ('hear_from', models.CharField(max_length=30)),
                ('special_request', models.TextField(blank=True, null=True)),
                ('other_classes', multiselectfield.db.fields.MultiSelectField(choices=[('Dance Classes', 'Dance Classes'), ('Music Classes', 'Music Classes')], max_length=15)),
                ('is_nepali_student', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='nepali_student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DanceStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signing_for', models.CharField(max_length=20)),
                ('parents_name', models.CharField(max_length=50)),
                ('dance_skills', models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('dance_style', models.CharField(choices=[('Nepali Classical Dance', 'Nepali Classical Dance'), ('Nepali Folk/Freestyle/Fusion', 'Nepali Folk/Freestyle/Fusion'), ('Indian Classical Dance', 'Indian Classical Dance'), ('Bollywood Dance', 'Bollywood Dance')], max_length=30)),
                ('session_type', models.CharField(choices=[('Group Class 1 seesion per week', 'Group Class 1 session per week'), ('Group Class 2 seesion per week', 'Group Class 2 session per week'), ('One-One class 1 session per week', 'One-One class 1 session per week'), ('One-One class 2 session per week', 'One-One class 2 session per week')], max_length=32)),
                ('class_time', multiselectfield.db.fields.MultiSelectField(choices=[('Sunday Morning', 'Sunday Morning'), ('Sunday Evening', 'Sunday Evening'), ('Monday Morning', 'Monday Morning'), ('Monday Evening', 'Monday Evening'), ('Tuesday Morning', 'Tuesday Morning'), ('Tuesday Evening', 'Tuesday Evening'), ('Wednesday Morning', 'Wednesday Morning'), ('Wednesday Evening', 'Wednesday Evening'), ('Thursday Morning', 'Thursday Morning'), ('Thursday Evening', 'Thursday Evening'), ('Friday Morning', 'Friday Morning'), ('Friday Evening', 'Friday Evening'), ('Saturday Morning', 'Saturday Morning'), ('Saturday Evening', 'Saturday Evening')], max_length=100)),
                ('goal_for_class', models.TextField(null=True)),
                ('hear_from', models.CharField(max_length=30)),
                ('special_request', models.TextField(blank=True, null=True)),
                ('other_classes', multiselectfield.db.fields.MultiSelectField(choices=[('Nepali Classes', 'Nepali Classes'), ('Music Classes', 'Music Classes')], max_length=15)),
                ('is_dance_student', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
