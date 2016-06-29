import responses
from django.conf import settings

class TimeTrackingAppMock(object):

    WORKTIME_CARD_ITEM_BASE = {
        'overtimeHours': {
            'saturday': {
                'hours': 0
            },
            'friday': {
                'hours': 0
            },
            'thursday': {
                'hours': 0
            },
            'wednesday': {
                'hours': 0
            },
            'tuesday': {
                'hours': 0
            },
            'monday': {
                'hours': 0
            },
            'sunday': {
                'hours': 0
            }
        },
        'workHours': {
            'saturday': {
                'timeRange': {
                    'start': '1970-01-01T00:00:00.000Z',
                    'end': '1970-01-01T00:00:00.000Z'
                },
                'hours': 0,
                'recordType': 'Not a Work Day'
            },
            'friday': {
                'timeRange': {
                    'start': '2016-03-17T12:00:18.057Z',
                    'end': '2016-03-17T22:00:18.057Z'
                },
                'hours': 10,
                'recordType': 'Work Day'
            },
            'thursday': {
                'timeRange': {
                    'start': '2016-03-17T12:00:18.057Z',
                    'end': '2016-03-17T22:00:18.057Z'
                },
                'hours': 10,
                'recordType': 'Work Day'
            },
            'wednesday': {
                'timeRange': {
                    'start': '2016-03-17T12:00:18.057Z',
                    'end': '2016-03-17T22:00:18.057Z'
                },
                'hours': 10,
                'recordType': 'Work Day'
            },
            'tuesday': {
                'timeRange': {
                    'start': '2016-03-17T12:00:18.057Z',
                    'end': '2016-03-17T22:30:18.057Z'
                },
                'hours': 10.5,
                'recordType': 'Work Day'
            },
            'monday': {
                'timeRange': {
                    'start': '1970-01-01T00:00:00.000Z',
                    'end': '1970-01-01T00:00:00.000Z'
                },
                'hours': 0,
                'recordType': 'Work Day'
            },
            'sunday': {
                'timeRange': {
                    'start': '1970-01-01T00:00:00.000Z',
                    'end': '1970-01-01T00:00:00.000Z'
                },
                'hours': 0,
                'recordType': 'Not a Work Day'
            }
        },
        'tags': [
            {
                'tagType': 'ByState',
                'tagContent': 'Indiana'
            }
        ]
    }


    WORKTIME_SHEET_RESPONSE_ITEM_BASE = {
        'weekStartDate': '2016-03-13T05:00:00.000Z',
        'updatedTimestamp': '2016-03-18T02:53:48.825Z',
        'createdTimestamp': '2016-03-18T02:53:48.824Z',
        'timecards': [],
        'employee': {
            'personDescriptor': 'BMHT_3_babf7c42f76af6f81486d76ff6e33505',
            'firstName': 'Simon',
            'lastName': 'Cowell',
            'email': 'user3@benefitmy.com',
            'companyDescriptor': 'BMHT_6_83a2f11c7e12d298ad466c63aa14c82f'
        }
    }


    def setup_mock_get(self, path, return_json, return_status=200):
        response_path = '{0}{1}'.format(settings.TIME_TRACKING_SERVICE_URL, path)
        responses.add(
            responses.GET,
            response_path,
            json=return_json,
            status=return_status,
            match_querystring=True)
