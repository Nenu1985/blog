# Generated by Django 2.2.2 on 2019-06-29 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='users_subscribe',
            new_name='subscribes',
        ),
    ]