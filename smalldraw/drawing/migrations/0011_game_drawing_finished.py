# Generated by Django 3.2.9 on 2021-12-30 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawing', '0010_alter_game_secret_word'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='drawing_finished',
            field=models.BooleanField(default=False),
        ),
    ]
