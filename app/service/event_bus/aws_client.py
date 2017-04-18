import boto3

from datetime import datetime
import threading
import logging

# How long would the client keep the boto3 session, until
# invalidate (and recreate) it, in seconds
AWS_CLIENT_BOTO3_SESSION_INVALIDATE_TIME = 3600


class AwsClient(object):
    def __init__(self, aws_region, aws_access_key_id, aws_secret_access_key):
        self._aws_region = aws_region
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key

        # boto3 constructs
        self._session = None
        self._session_timestamp = None
        self._sqs = None
        self._sns = None

    @property
    def sqs(self):
        self._ensure_active_session()
        return self._sqs
    
    @property
    def sns(self):
        self._ensure_active_session()
        return self._sns

    def _ensure_active_session(self):
        # Use double-locking pattern to ensure the reset
        # session logic is thread-safe
        if (self._session_require_reset()):
            with threading.Lock():
                if (self._session_require_reset()):
                    self._session = boto3.session.Session(
                        aws_access_key_id=self._aws_access_key_id,
                        aws_secret_access_key=self._aws_secret_access_key,
                        region_name=self._aws_region)
                    self._session_timestamp = datetime.now()

                    # initialize the clients
                    self._sns = self._session.client('sns')
                    self._sqs = self._session.resource('sqs')

                    logging.info('Boto3 session recreated.')

    def _session_require_reset(self):
        return self._session is None or self._session_expired()

    def _session_expired(self):
        if (self._session_timestamp is None):
            return True
        now = datetime.now()
        delta = now - self._session_timestamp
        return delta.total_seconds() >= AWS_CLIENT_BOTO3_SESSION_INVALIDATE_TIME
