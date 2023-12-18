from rest_framework import serializers

from .models import Exclusion, User, Draw


class ExclusionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exclusion
        fields = ['recipient', 'target']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']


class DrawSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Draw
        fields = ['id', 'timestamp']
