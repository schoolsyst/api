# Generated by Django 2.2.4 on 2019-08-14 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20190806_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
