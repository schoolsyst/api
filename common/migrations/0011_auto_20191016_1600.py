# Generated by Django 2.2.6 on 2019-10-16 16:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_auto_20191012_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='abbreviation',
            field=models.CharField(max_length=3, validators=[django.core.validators.RegexValidator('[^\\s]{,3}', 'Please use at most 3 non-space characters')]),
        ),
    ]
