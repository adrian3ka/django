# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

class MasterDegrees(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterFacilities(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterFields(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterIndustries(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterJobLevels(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterLocations(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterMajors(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterSkillSets(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name.title()
# Create your models here.

class UserAnswer(models.Model):
    category = models.CharField(max_length=255, blank=True, default='')
    text = models.CharField(blank=False, default='',  max_length=255)

    class Meta:
        unique_together = ('category', 'text')
    def __str__(self):
        return self.text

class BotQuestion(models.Model):
    category = models.CharField(max_length=255, blank=True, default='')
    text = models.CharField(blank=False, default='', max_length=255)
        
    class Meta:
        unique_together = ('category', 'text')
    def __str__(self):
        return self.text
