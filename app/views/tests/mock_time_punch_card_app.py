import responses
from django.conf import settings

class TimePunchCardAppMock(object):

    PUNCH_CARD_BASE = {
        '_id': '5871b2222d27d72d1a792f76',
        'date': '2017-01-03T05:00:00.000Z',
        'employee': {  
            'email' : 'user3@benefitmy.com',
            'firstName': 'Simon',
            'lastName': 'Cowell',
            'personDescriptor': 'localhost_BMHT_3_babf7c42f76af6f81486d76ff6e33505',
            'companyDescriptor': 'localhost_BMHT_1_b457df460695969e8960e3f1623a3ee7'
        },
        'attributes': [],
        'start': '2017-01-03T13:00:00.000Z',
        'end': '2017-01-03T15:30:00.000Z',
        'inHours': 'false',
        'recordType': 'Work Time',
        'createdTimestamp': '2017-01-08T03:29:38.127Z',
        'updatedTimestamp': '2017-01-08T03:29:38.127Z'
    }

    def setup_mock_get(self, path, return_json, return_status=200):
        response_path = '{0}{1}'.format(settings.TIME_TRACKING_SERVICE_URL, path)
        responses.add(
            responses.GET,
            response_path,
            json=return_json,
            status=return_status,
            match_querystring=True)
