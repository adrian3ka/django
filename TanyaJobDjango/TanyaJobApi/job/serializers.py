from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
	class Meta:
		model = Job
		fields = ('id', 'title', 'degree', 'major', 'industry', 'min_age', 'max_age', 'field', 'location', 'job_level', 'work_exp', 'min_salary', 'max_salary')
