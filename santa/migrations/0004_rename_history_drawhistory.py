# Generated by Django 5.0 on 2023-12-17 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('santa', '0003_draw_ban_target_alter_ban_recipient_history'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='History',
            new_name='DrawHistory',
        ),
    ]
