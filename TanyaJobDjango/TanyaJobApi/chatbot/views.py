# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import UserAnswer, BotQuestion
from .serializers import UserAnswerSerializer, BotQuestionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import random
from .levenshtein import LevenshteinExtraction

levenshtein = LevenshteinExtraction()

class DefaultsMixin(object):
	"""Default settings for view authentication, permissions,
	filtering and pagination."""
	"""
	authentication_classes = (
		authentication.BasicAuthentication,
		authentication.TokenAuthentication,
	)
	permission_classes = (
		permissions.IsAuthenticated,
	)
	"""
	paginate_by = 25
	paginate_by_param = 'page_size'
	max_paginate_by = 100

class UserAnswerViewSet(viewsets.ModelViewSet):
	"""API endpoint for listing and creating sprints."""
	queryset = UserAnswer.objects.order_by('id')
	serializer_class = UserAnswerSerializer

class BotQuestionViewSet(viewsets.ModelViewSet):
	"""API endpoint for listing and creating sprints."""
	queryset = BotQuestion.objects.order_by('id')
	serializer_class = BotQuestionSerializer

@api_view(['POST'])
def ExtractInformation(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    info = levenshtein.extract(body['category'], body['text'])
    return Response({"message": info})

@api_view(['POST'])
def AskQuestion(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    question = BotQuestion.objects.filter(category = body['category'])
    randomNumber = random.randint(0, len(question) - 1)
    return Response({"question": str(question[randomNumber])})
