# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-25 09:06
from __future__ import unicode_literals

from django.db import migrations, models
import music.models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0010_auto_20160918_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_logo',
            field=models.FileField(default='settings.MEDIA_ROOT/default.jpg', upload_to=music.models.content_file_name),
        ),
    ]
