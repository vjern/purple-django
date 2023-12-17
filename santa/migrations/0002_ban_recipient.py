# Generated by Django 5.0 on 2023-12-17 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('santa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ban',
            name='recipient',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='santa.user'),
            preserve_default=False,
        ),
    ]
