# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import UserAnswer, BotQuestion, MasterDegrees, MasterFacilities, MasterFields, MasterIndustries, MasterJobLevels, MasterLocations, MasterMajors, MasterSkillSets
from .serializers import UserAnswerSerializer, BotQuestionSerializer, MasterDegreesSerializer, MasterFacilitiesSerializer, MasterFieldsSerializer, MasterIndustriesSerializer, MasterJobLevelsSerializer, MasterLocationsSerializer, MasterMajorsSerializer, MasterSkillSetsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import random
from .levenshtein import LevenshteinExtraction
from .WordTagger import TextTagger


with open('./data_source.json') as f:
    data_source = json.load(f)

levenshtein = LevenshteinExtraction()
tagger = TextTagger(data_source["text_tagger"])


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


class MasterDegreesViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""
    queryset = MasterDegrees.objects.order_by('id')
    serializer_class = MasterDegreesSerializer


class MasterFacilitiesViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""
    queryset = MasterFacilities.objects.order_by('id')
    serializer_class = MasterFacilitiesSerializer


class MasterFieldsViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""
    queryset = MasterFields.objects.order_by('id')
    serializer_class = MasterFieldsSerializer


class MasterIndustriesViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""
    queryset = MasterIndustries.objects.order_by('id')
    serializer_class = MasterIndustriesSerializer


class MasterJobLevelsViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""
    queryset = MasterJobLevels.objects.order_by('id')
    serializer_class = MasterJobLevelsSerializer


class MasterLocationsViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""
    queryset = MasterLocations.objects.order_by('id')
    serializer_class = MasterLocationsSerializer


class MasterMajorsViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""
    queryset = MasterMajors.objects.order_by('id')
    serializer_class = MasterMajorsSerializer


class MasterSkillSetsViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""
    queryset = MasterSkillSets.objects.order_by('id')
    serializer_class = MasterSkillSetsSerializer


@api_view(['POST'])
def ExtractInformation(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    info = levenshtein.extract(body['category'], body['text'])
    return Response({"message": info})


@api_view(['POST'])
def ExtractInformationV2(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    result = tagger.getTagger(body['text'])
    extracted = []
    for idx, val in enumerate(result):
        if val[1] == 'NN' or (idx > 0 and result[idx-1][1] == 'NN'):
            extracted += val[0] + ' '
    extracted = ''.join(extracted)
    result = None
    info, typo_correction, suggested_word = levenshtein.template_matching(
        body['category'], extracted)
    return Response({
        "message": info,
        "typo_correction": typo_correction,
        "suggested_word": suggested_word
    })


@api_view(['POST'])
def AskQuestion(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    question = BotQuestion.objects.filter(category=body['category'])
    if len(question) == 0:
        return Response(
            {"question": body['category'] + " Category Still Empty"})
    randomNumber = random.randint(0, len(question) - 1)
    return Response({"question": str(question[randomNumber])})
