from rest_framework import serializers

from .models import *


class UserdataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'


class ChatdataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
