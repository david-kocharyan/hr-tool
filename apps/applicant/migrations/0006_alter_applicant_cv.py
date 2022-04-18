# Generated by Django 4.0.3 on 2022-04-18 12:45

import apps.applicant.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0005_alter_applicant_comment_alter_applicant_cv_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='cv',
            field=models.FileField(null=True, upload_to=apps.applicant.models.post_directory_path, validators=[django.core.validators.FileExtensionValidator(['pdf', 'csv', 'png', 'jpg']), apps.applicant.models.validate_file_size], verbose_name='CV'),
        ),
    ]
