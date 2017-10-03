from rest_framework import serializers

class FieldWithIdOrObject(serializers.WritableField):
    model = None
    serializer = None

    def to_native(self, obj):
        if obj:
            return obj.id
        else:
            return None


    def from_native(self, data):
        if not data:
            return None
        elif isinstance(data, unicode) and self.model:
            return self.model.objects.get(id=int(data))
        elif self.serializer:
            return self.serializer(data=data).object
        else:
            return None
