# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

class MasterDegree(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterFacility(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterField(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterIndustry(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterJobLevel(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterLocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterMajor(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

class MasterSkillSet(models.Model):
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
