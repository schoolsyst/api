# Generated by Django 2.2.4 on 2019-08-14 18:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0005_auto_20190814_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='actual',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, "This can't be a negative value"), django.core.validators.MaxValueValidator(1, 'This should be a value between 0 and 1')]),
        ),
        migrations.AlterField(
            model_name='grade',
            name='expected',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, "This can't be a negative value"), django.core.validators.MaxValueValidator(1, 'This should be a value between 0 and 1')]),
        ),
        migrations.AlterField(
            model_name='grade',
            name='goal',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, "This can't be a negative value"), django.core.validators.MaxValueValidator(1, 'This should be a value between 0 and 1')]),
        ),
        migrations.AlterField(
            model_name='note',
            name='filepath',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='notion',
            name='progress',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, "This can't be a negative value"), django.core.validators.MaxValueValidator(1, 'This should be a value between 0 and 1')]),
        ),
    ]
