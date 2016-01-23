import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class LoggingServiceTests(TestCase, ViewTestBase):

    def test_post_log_record(self):
        data = {
            "type": "POST",
            "url": "http://app.workbenefits.me/",
            "contentType": "application/json",
            "data": {
                "url": "http://app.workbenefits.me/login",
                "message": "errorMessage",
                "browser": "BrowserDetectionService",
                "type": "exception",
                "stackTrace": "THIS IS A STACKTRACE"
            }
        }
        response = self.client.post(reverse('logging_api',
                                            kwargs={'level': "error"}),
                                            data=json.dumps(data),
                                            content_type='application/json')

        self.assertIsNotNone(response)

        print response
        self.assertEqual(response.status_code, 201)

    def test_post_log_record_with_wrong_level(self):
        data = {
            "type": "POST",
            "url": "http://app.workbenefits.me/",
            "contentType": "application/json",
            "data": {
                "url": "http://app.workbenefits.me/login",
                "message": "errorMessage",
                "browser": "BrowserDetectionService",
                "type": "exception",
                "stackTrace": "THIS IS A STACKTRACE"
            }
        }
        response = self.client.post(reverse('logging_api',
                                            kwargs={'level': "NOTVALID"}),
                                            data=json.dumps(data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
