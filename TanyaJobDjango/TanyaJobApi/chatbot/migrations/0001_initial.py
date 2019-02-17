# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-30 05:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='BotQuestion',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('category',
                 models.CharField(blank=True, default=b'', max_length=255)),
                ('text', models.CharField(default=b'', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('category',
                 models.CharField(blank=True, default=b'', max_length=255)),
                ('text', models.CharField(default=b'', max_length=255)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='useranswer',
            unique_together=set([('category', 'text')]),
        ),
        migrations.AlterUniqueTogether(
            name='botquestion',
            unique_together=set([('category', 'text')]),
        ),
    ]
