# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 11:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20161019_1922'),
    ]

    operations = [
        migrations.RenameField(
            model_name='component',
            old_name='module_ID',
            new_name='module',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='catagory_ID',
            new_name='catagory',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='instructor_ID',
            new_name='instructor',
        ),
        migrations.RenameField(
            model_name='currentenrollment',
            old_name='course_ID',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='currentenrollment',
            old_name='participant_ID',
            new_name='participant',
        ),
        migrations.RenameField(
            model_name='historyenrollment',
            old_name='course_ID',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='historyenrollment',
            old_name='participant_ID',
            new_name='participant',
        ),
        migrations.RenameField(
            model_name='module',
            old_name='course_ID',
            new_name='course',
        ),
    ]
