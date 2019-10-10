# Generated by Django 2.2.4 on 2019-10-09 20:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0025_auto_20191009_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=300)),
                ('notes', models.TextField(blank=True, null=True)),
                ('due', models.DateTimeField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework', to='common.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=300)),
                ('obtained', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, "This can't be a negative value"), django.core.validators.MaxValueValidator(1, 'This should be a value between 0 and 1')], verbose_name='Obtained grade')),
                ('expected', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, "This can't be a negative value"), django.core.validators.MaxValueValidator(1, 'This should be a value between 0 and 1')], verbose_name='Expected grade')),
                ('goal', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, "This can't be a negative value"), django.core.validators.MaxValueValidator(1, 'This should be a value between 0 and 1')], verbose_name='Grade goal')),
                ('unit', models.FloatField(default=20, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Grade unit')),
                ('weight', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Grade weight')),
                ('homework', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homework', to='homework.Homework')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='common.Subject')),
            ],
        ),
    ]
