from rest_framework import serializers
from .models import UserAnswer, BotQuestion

class UserAnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserAnswer
		fields = ('id', 'category', 'text',)

class BotQuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = BotQuestion
		fields = ('id', 'category', 'text',)
