# Generated by Django 2.2.4 on 2019-08-25 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0020_auto_20190823_1335'),
        ('learn', '0021_note_filetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='common.Subject'),
            preserve_default=False,
        ),
    ]
