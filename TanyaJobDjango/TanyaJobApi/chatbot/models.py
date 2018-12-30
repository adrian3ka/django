# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


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
