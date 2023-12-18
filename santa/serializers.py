from rest_framework import serializers

from .models import Exclusion, User


class ExclusionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exclusion
        fields = ['recipient', 'target']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['name']