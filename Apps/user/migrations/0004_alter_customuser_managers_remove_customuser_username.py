# Generated by Django 5.1.4 on 2025-01-11 04:46

import user.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_customuser_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', user.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]