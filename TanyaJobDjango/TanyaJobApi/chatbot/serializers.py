from rest_framework import serializers
from .models import UserAnswer, BotQuestion, MasterDegrees, MasterFacilities, MasterFields, MasterIndustries, MasterJobLevels, MasterLocations, MasterMajors, MasterSkillSets


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = (
            'id',
            'category',
            'text',
        )


class BotQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotQuestion
        fields = (
            'id',
            'category',
            'text',
        )


class MasterDegreesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterDegrees
        fields = ('id', 'name')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self':
            reverse(
                'maste-degrees-detail', kwargs={'pk': obj.pk},
                request=request),
        }


class MasterFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterFacilities
        fields = ('id', 'name')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self':
            reverse(
                'maste-facilities-detail',
                kwargs={'pk': obj.pk},
                request=request),
        }


class MasterFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterFields
        fields = ('id', 'name')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self':
            reverse(
                'maste-fields-detail', kwargs={'pk': obj.pk}, request=request),
        }


class MasterIndustriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterIndustries
        fields = ('id', 'name')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self':
            reverse(
                'maste-industries-detail',
                kwargs={'pk': obj.pk},
                request=request),
        }


class MasterJobLevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterJobLevels
        fields = ('id', 'name')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self':
            reverse(
                'maste-job-levels-detail',
                kwargs={'pk': obj.pk},
                request=request),
        }


class MasterLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterLocations
        fields = ('id', 'name')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self':
            reverse(
                'maste-locations-detail',
                kwargs={'pk': obj.pk},
                request=request),
        }


class MasterMajorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterMajors
        fields = ('id', 'name')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self':
            reverse(
                'maste-majors-detail', kwargs={'pk': obj.pk}, request=request),
        }


class MasterSkillSetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterSkillSets
        fields = ('id', 'name')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self':
            reverse(
                'maste-majors-detail', kwargs={'pk': obj.pk}, request=request),
        }
