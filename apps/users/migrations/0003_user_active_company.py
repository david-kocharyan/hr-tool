# Generated by Django 4.0.3 on 2022-03-11 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_forgetpassword'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active_company',
            field=models.PositiveBigIntegerField(null=True, verbose_name='Active Company'),
        ),
    ]
