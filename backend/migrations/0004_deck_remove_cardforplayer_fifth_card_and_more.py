# Generated by Django 5.0 on 2024-01-01 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_game_id_cardforplayer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cards', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='cardforplayer',
            name='fifth_card',
        ),
        migrations.RemoveField(
            model_name='cardforplayer',
            name='first_card',
        ),
        migrations.RemoveField(
            model_name='cardforplayer',
            name='fourth_card',
        ),
        migrations.RemoveField(
            model_name='cardforplayer',
            name='second_card',
        ),
        migrations.RemoveField(
            model_name='cardforplayer',
            name='third_card',
        ),
        migrations.AddField(
            model_name='cardforplayer',
            name='cards',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]