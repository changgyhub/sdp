# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='component',
            name='content',
        ),
        migrations.RemoveField(
            model_name='component',
            name='content_file',
        ),
        migrations.RemoveField(
            model_name='component',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='component',
            name='module',
        ),
    ]