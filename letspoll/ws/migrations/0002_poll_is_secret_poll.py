# Generated by Django 2.2.4 on 2019-08-07 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ws', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='is_secret_poll',
            field=models.BooleanField(default=False),
        ),
    ]