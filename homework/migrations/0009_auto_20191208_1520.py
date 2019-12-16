# Generated by Django 2.2.6 on 2019-12-08 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0008_auto_20191208_1520'),
        ('homework', '0008_auto_20191107_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='date_obtained',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='homework',
        ),
        migrations.AddField(
            model_name='homework',
            name='grades',
            field=models.ManyToManyField(to='homework.Grade'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='obtained',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='homework',
            name='notes',
        ),
        migrations.AddField(
            model_name='homework',
            name='notes',
            field=models.ManyToManyField(to='learn.Note'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='type',
            field=models.CharField(choices=[('TEST', 'Contrôle'), ('COURSEWORK', 'Devoir maison'), ('EXERCISE', 'Exercice'), ('TOBRING', 'À apporter')], max_length=2, verbose_name='Type'),
        ),
    ]