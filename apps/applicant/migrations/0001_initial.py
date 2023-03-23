# Generated by Django 4.0.3 on 2022-11-04 14:15

import apps.applicant.models
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=50, verbose_name='First name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last name')),
                ('email', models.EmailField(max_length=125, verbose_name='Email')),
                ('phone', models.CharField(max_length=30, verbose_name='Phone')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male', max_length=20, verbose_name='Gender')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('dob', models.DateField(verbose_name='Date of Birth')),
                ('level', models.TextField(choices=[('junior', 'Junior'), ('middle', 'Middle'), ('senior', 'Senior'), ('team_lead', 'Team lead')], default='junior', max_length=50, verbose_name='Level')),
                ('skill', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50, null=True), size=None, verbose_name='Skills')),
                ('comment', models.TextField(max_length=2000, verbose_name='Comment')),
                ('status', models.CharField(choices=[('shortlisted', 'Shortlisted'), ('not_considered', 'Not considered'), ('interviewing', 'Interviewing'), ('rejected', 'Rejected'), ('for_future_consideration', 'For future consideration'), ('black_list', 'Black list')], default='shortlisted', max_length=60, verbose_name='Status')),
                ('cv', models.FileField(null=True, upload_to=apps.applicant.models.post_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'csv', 'png', 'jpg', 'doc', 'docx']), apps.applicant.models.validate_file_size], verbose_name='CV')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
