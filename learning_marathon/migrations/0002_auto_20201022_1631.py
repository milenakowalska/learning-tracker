# Generated by Django 3.0.2 on 2020-10-22 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_marathon', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='learningsession',
            old_name='udemy',
            new_name='theory',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='udemy',
            new_name='theory',
        ),
    ]
