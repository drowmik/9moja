# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-07 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_scrapper', '0006_scrappeddata'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrappeddata',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scrappeddata',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scrappeddata',
            name='shares',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
