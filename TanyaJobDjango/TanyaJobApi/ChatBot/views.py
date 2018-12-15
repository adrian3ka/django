# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import UserAnswer, BotQuestion
from .serializers import UserAnswerSerializer, BotQuestionSerializer

class UserAnswerViewSet(viewsets.ModelViewSet):
	"""API endpoint for listing and creating sprints."""
	queryset = UserAnswer.objects.order_by('id')
	serializer_class = UserAnswerSerializer

class BotQuestionViewSet(viewsets.ModelViewSet):
	"""API endpoint for listing and creating sprints."""
	queryset = BotQuestion.objects.order_by('id')
	serializer_class = BotQuestionSerializer
