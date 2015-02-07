from rest_framework import serializers
from app.models.fsa import FSA


class FSASerializer(serializers.ModelSerializer):

    class Meta:
        model = FSA
