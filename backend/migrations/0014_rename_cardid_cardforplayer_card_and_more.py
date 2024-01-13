# Generated by Django 5.0 on 2024-01-13 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_remove_cardforplayer_cards_cardforplayer_cardid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cardforplayer',
            old_name='cardID',
            new_name='card',
        ),
        migrations.RenameField(
            model_name='cardforplayer',
            old_name='playerID',
            new_name='player',
        ),
        migrations.RenameField(
            model_name='cardfromdeck',
            old_name='cardID',
            new_name='card',
        ),
        migrations.RenameField(
            model_name='cardfromdeck',
            old_name='deckID',
            new_name='deck',
        ),
        migrations.RenameField(
            model_name='deck',
            old_name='gameID',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='gameID',
            new_name='game',
        ),
    ]
