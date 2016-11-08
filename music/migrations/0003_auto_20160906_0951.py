# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-06 06:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_song_song_duration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='song_titile',
            new_name='song_title',
        ),
        migrations.RemoveField(
            model_name='song',
            name='file_type',
        ),
        migrations.RemoveField(
            model_name='song',
            name='song_duration',
        ),
        migrations.AddField(
            model_name='song',
            name='audio_file',
            field=models.FileField(default=b'', upload_to=b''),
        ),
        migrations.AddField(
            model_name='song',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
