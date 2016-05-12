from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.workers_comp.phraseology import Phraseology


class PhraseologySerializer(HashPkSerializerBase):
    class Meta:
        model = Phraseology
