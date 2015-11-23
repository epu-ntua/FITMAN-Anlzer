__author__ = 'mpetyx'

from django.contrib.auth.models import Group
from rest_framework import serializers

from UIapp.models import Team, Project, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = Team
        fields = ('url', 'name', 'created_by', 'created')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    # owned_by = serializers.HyperlinkedRelatedField(many=True, view_name='user', read_only=True)

    owned_by = TeamSerializer()
    created_by = UserSerializer()

    class Meta:
        model = Project
        fields = ('url', 'name', 'created_by', 'owned_by', 'created')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
