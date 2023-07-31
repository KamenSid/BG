from rest_framework import serializers
from .models import Replay


class ReplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Replay
        fields = '__all__'
