# Generated by Django 4.1 on 2022-08-22 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_myplaylist_is_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myplaylist',
            name='is_public',
        ),
    ]