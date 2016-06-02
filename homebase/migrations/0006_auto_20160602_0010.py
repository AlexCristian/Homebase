# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-02 00:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebase', '0005_auto_20160601_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='type',
            field=models.CharField(choices=[('GP', 'Group project'), ('LB', 'Lab'), ('PP', 'Paper'), ('DP', 'Discussion post')], max_length=2),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='recurs',
            field=models.CharField(choices=[('M', 'Monthly'), ('W', 'Weekly'), ('B', 'Bi-weekly')], max_length=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=200, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password_sha1',
            field=models.CharField(max_length=41),
        ),
    ]
