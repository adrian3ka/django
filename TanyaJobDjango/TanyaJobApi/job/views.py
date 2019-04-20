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
LIMIT_JOB_TITLE = 5

# Create your views here.
class JobViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""
    queryset = Job.objects.order_by('id')
    serializer_class = JobSerializer


@api_view(['POST'])
def GetJobRecommendation(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    title = hotModel.decide(body)

    limit = body["limit"]
    offset = body["offset"]

    cursor = connection.cursor()

    data = []

    generated_title = []
    for t in title:
        generated_title.append("'" + t + "'")

    generated_title = (', ').join(generated_title)
    print generated_title
    # Data retrieval operation - no commit required
    cursor.execute("SELECT original_title, link FROM job_job WHERE title IN (" + generated_title + ") GROUP BY link ORDER BY FIELD(title," + generated_title + ") LIMIT " + str(limit) + " OFFSET " + str(offset))
    records = cursor.fetchall()

    returned_title = []
    over = False
    for row in records:
        if len(returned_title) <= LIMIT_JOB_TITLE:
            returned_title.append(row[0].lower())
        else:
            over = True
        data.append({"title": row[0], "link": row[1]})

    cursor.execute("SELECT COUNT(*) FROM (SELECT COUNT(*) FROM job_job WHERE title IN (" + generated_title + ") GROUP BY link) x")
    records = cursor.fetchone()

    count = records[0]

    cursor.close()

    returned_title = set(returned_title)
    returned_title_final = [] 
    for t in returned_title:
        returned_title_final.append(t.title())
    if over:
        returned_title_final.append("dan lainnya")
    return Response({"job_title": returned_title_final, "data": data, "total": count})

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
