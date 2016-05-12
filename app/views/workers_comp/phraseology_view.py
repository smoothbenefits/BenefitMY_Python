from rest_framework.views import APIView
from rest_framework.response import Response

from app.models.workers_comp.phraseology import Phraseology
from app.serializers.workers_comp.phraseology_serializer import \
    PhraseologySerializer


class AllPhraseologyView(APIView):

    def get(self, request, format=None):
        all_phraseologys = Phraseology.objects.all()
        serializer = PhraseologySerializer(all_phraseologys, many=True)
        return Response(serializer.data)
