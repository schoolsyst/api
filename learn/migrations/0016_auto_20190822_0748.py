# Generated by Django 2.2.4 on 2019-08-22 07:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0015_note_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='note',
            name='last_modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'),
        ),
    ]