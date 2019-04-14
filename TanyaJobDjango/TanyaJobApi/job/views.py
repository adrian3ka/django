# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from django.shortcuts import render
from .models import Job
from .serializers import JobSerializer
from .decision_tree import JobRecommendationDecisionTree
from .hot_decision_tree import HotJobRecommendationDecisionTree
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
import json

model = JobRecommendationDecisionTree()
hotModel = HotJobRecommendationDecisionTree()


# Create your views here.
class JobViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""
    queryset = Job.objects.order_by('id')
    serializer_class = JobSerializer


@api_view(['POST'])
def GetJobRecommendation(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    data = hotModel.decide(body)
    return Response({"job_title": data})

@api_view(['GET'])
def GetJob(request):
    limit = request.GET.get("limit")
    title = request.GET.get("title")
    offset = request.GET.get("offset")
    print title, limit, offset
    queryset = Job.objects.filter(title= title).order_by('id')[offset:limit].values()
    return Response(queryset)
