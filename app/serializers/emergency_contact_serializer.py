from rest_framework import serializers
from app.models.emergency_contact import EmergencyContact


class EmergencyContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmergencyContact
