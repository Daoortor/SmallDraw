# Generated by Django 3.2.9 on 2021-12-07 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawing', '0005_rename_category_word_category_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='secret_word',
            field=models.CharField(default='', max_length=32),
        ),
    ]