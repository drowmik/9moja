# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-28 11:56
from __future__ import unicode_literals

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0036_auto_20171226_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=main_app.models.get_image_path),
        ),
    ]
