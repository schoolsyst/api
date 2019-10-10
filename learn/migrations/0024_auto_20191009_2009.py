# Generated by Django 2.2.4 on 2019-10-09 20:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0025_auto_20191009_2009'),
        ('learn', '0023_auto_20190908_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='Learndata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('data', models.TextField(blank=True, null=True, verbose_name='YAML Content')),
                ('name', models.CharField(max_length=300)),
                ('learnt', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0, "This can't be a negative value"), django.core.validators.MaxValueValidator(1, 'This should be a value between 0 and 1')], verbose_name='Learning progress')),
                ('test_tries', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tries in testing mode')),
                ('train_tries', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tries in training mode')),
                ('last_opened', models.DateTimeField(auto_now=True)),
                ('time_spent', models.DurationField(verbose_name='Time spent on learning')),
            ],
        ),
        migrations.RemoveField(
            model_name='test',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='test',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='note',
            name='learnt',
        ),
        migrations.AlterField(
            model_name='note',
            name='filetype',
            field=models.CharField(choices=[('MARKDOWN', 'Markdown'), ('ASCIIDOC', 'AsciiDoc'), ('STUDENTML', 'StudentML')], default=('MARKDOWN', 'Markdown'), max_length=50),
        ),
        migrations.AlterField(
            model_name='note',
            name='name',
            field=models.CharField(max_length=300),
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AddField(
            model_name='learndata',
            name='note',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='learndatas', to='learn.Note'),
        ),
        migrations.AddField(
            model_name='learndata',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learndatas', to='common.Subject'),
        ),
    ]
