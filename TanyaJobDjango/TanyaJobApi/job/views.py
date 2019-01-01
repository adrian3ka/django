# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from django.shortcuts import render
from .models import Job
from .serializers import JobSerializer
from .decision_tree import JobRecommendationDecisionTree
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

# Create your views here.
class JobViewSet(viewsets.ModelViewSet):
	"""API endpoint for listing and creating sprints."""
	queryset = Job.objects.order_by('id')
	serializer_class = JobSerializer

@api_view(['POST'])
def GetJobRecommendation(request):
    model = JobRecommendationDecisionTree()
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    data = model.decide(body)
    print "---------------------------"
    print data
    print "---------------------------"
    return Response({"message": data})
