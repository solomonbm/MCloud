# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-08 05:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_auto_20160907_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_logo',
            field=models.FileField(default=b'static/music/images/album_logos/default.jpg', upload_to=b''),
        ),
    ]
