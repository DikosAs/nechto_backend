# Generated by Django 5.0 on 2024-01-08 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_alter_player_options_alter_card_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='type',
            field=models.CharField(choices=[('ACT', 'Активная'), ('DEF', 'Защитная')], default='ACT', max_length=3, verbose_name='Тип'),
        ),
    ]
