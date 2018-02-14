import json
import reversion
import decimal

from django.db import models
from app.custom_authentication import AuthUser
from ..address import STATES_CHOICES
from app.serializers.tax.state_tax_election_serializer_factory import StateTaxElectionSerializerFactory
from app.dtos.tax.import_state_tax_election import ImportStateTaxElection


@reversion.register
class EmployeeStateTaxElection(models.Model):
    user = models.ForeignKey(AuthUser,
                             related_name="user_state_tax_elections")
    state = models.CharField(choices=STATES_CHOICES,
                             default='MA',
                             max_length=3)

    # This is to hold JSON representation of tax witholding data
    # Our current version of Django does not support Postgres JSONB
    # fields, so we are forced to just use text field. 
    # This should be ok for the purpose, as we do not expect queryability 
    # against the field values. 
    data = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = (('user', 'state'),)

    _state_tax_election_serializer_factory = StateTaxElectionSerializerFactory()

    @property
    def tax_election_data(self):
        if (not self.data):
            return None
        json_data = json.loads(self.data)

        # Below is to handle the case of imported tax election record
        # The expectation is that all imported election record would have
        # a 'metadata' property that has a 'data_source' member with value
        # 'import'
        imported = False
        if ('metadata' in json_data):
            if ('data_source' in json_data['metadata']):
                imported = json_data['metadata']['data_source'] == 'import'

        serializer = self._state_tax_election_serializer_factory.get_state_tax_election_serializer(self.state, imported)(data=json_data)
        if (not serializer.is_valid()):
            raise RuntimeError('Failed to deserialize state tax election data for user "{0}" and state "{1}": '.format(self.user.id, self.state), serializer.errors)
        return serializer.object

    @tax_election_data.setter
    def tax_election_data(self, value):
        if (not value):
            self.data = None

        imported = isinstance(value, ImportStateTaxElection)

        serializer = self._state_tax_election_serializer_factory.get_state_tax_election_serializer(self.state, imported)(value)
        self.data = json.dumps(serializer.data, cls=DecimalEncoder)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)