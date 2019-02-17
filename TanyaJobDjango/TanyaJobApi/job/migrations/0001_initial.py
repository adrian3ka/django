# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-31 07:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('title',
                 models.CharField(blank=True, default='', max_length=255)),
                ('degree',
                 models.CharField(blank=True, default='', max_length=255)),
                ('major',
                 models.CharField(blank=True, default='', max_length=255)),
                ('industry',
                 models.CharField(blank=True, default='', max_length=255)),
                ('age', models.SmallIntegerField(default=55)),
                ('field',
                 models.CharField(blank=True, default='', max_length=255)),
                ('location',
                 models.CharField(blank=True, default='', max_length=255)),
                ('job_level',
                 models.CharField(blank=True, default='', max_length=255)),
                ('work_exp', models.BigIntegerField(blank=True, default=0)),
                ('min_salary', models.BigIntegerField(blank=True, default=0)),
                ('max_salary', models.BigIntegerField(blank=True, default=0)),
            ],
        ),
    ]
