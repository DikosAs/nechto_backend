# Generated by Django 5.0 on 2024-01-08 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_rename_descriptin_card_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={},
        ),
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(max_length=32, verbose_name='Название'),
        ),
    ]
