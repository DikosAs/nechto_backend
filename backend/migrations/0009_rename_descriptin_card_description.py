# Generated by Django 5.0 on 2024-01-02 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_card_function_delete_cardfunction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='descriptin',
            new_name='description',
        ),
    ]
