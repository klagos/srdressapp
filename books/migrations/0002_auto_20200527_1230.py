# Generated by Django 3.0.5 on 2020-05-27 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='puntuacion',
            old_name='puntuacion',
            new_name='punt',
        ),
    ]
