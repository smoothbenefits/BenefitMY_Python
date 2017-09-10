from rest_framework import serializers


class StateTaxElectionSerializer(serializers.Serializer):

    def restore_object(self, attrs, instance=None):
        raise NotImplementedError('This needs to be implemented by concrete implementation!')
