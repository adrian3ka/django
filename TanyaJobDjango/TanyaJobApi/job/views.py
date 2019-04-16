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
from django.db import connection, transaction
import json
from django.db import connection, transaction
import MySQLdb

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
    cursor = connection.cursor()

    data = []
    # Data retrieval operation - no commit required
    cursor.execute("SELECT title, link FROM job_job WHERE title LIKE '" + title + "' GROUP BY link LIMIT " + limit + " OFFSET " + offset)
    records = cursor.fetchall()

    for row in records:
        data.append({"title": row[0], "link": row[1]})
    cursor.close()


    return Response({"code": 200, "data": data})
