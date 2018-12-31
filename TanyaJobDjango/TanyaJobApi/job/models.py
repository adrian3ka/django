# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=255, blank=True, default='')
    degree = models.CharField(max_length=255, blank=True, default='')
    major = models.CharField(max_length=255, blank=True, default='')
    industry = models.CharField(max_length=255, blank=True, default='')
    min_age = models.SmallIntegerField(default=18)
    max_age = models.SmallIntegerField(default=55)
    field = models.CharField(max_length=255, blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    job_level = models.CharField(max_length=255, blank=True, default='')
    work_exp = models.BigIntegerField(default=0, blank=True)
    min_salary = models.BigIntegerField(default=0, blank=True)
    max_salary = models.BigIntegerField(default=0, blank=True)

    def __str__(self):
        return self.title
