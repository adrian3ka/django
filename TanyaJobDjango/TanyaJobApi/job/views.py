# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from django.shortcuts import render
from .models import Job
from .serializers import JobSerializer

# Create your views here.
class JobViewSet(viewsets.ModelViewSet):
	"""API endpoint for listing and creating sprints."""
	queryset = Job.objects.order_by('id')
	serializer_class = JobSerializer
