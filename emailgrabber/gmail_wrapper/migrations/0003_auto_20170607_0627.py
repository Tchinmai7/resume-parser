# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-07 06:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmail_wrapper', '0002_auto_20170606_1828'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.AddField(
            model_name='pagestowatch',
            name='page_url',
            field=models.URLField(default='http://www.getmailage.com'),
            preserve_default=False,
        ),
    ]
