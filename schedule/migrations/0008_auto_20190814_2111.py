# Generated by Django 2.2.4 on 2019-08-14 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_auto_20190814_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addition',
            name='date',
            field=models.DateField(),
        ),
    ]
