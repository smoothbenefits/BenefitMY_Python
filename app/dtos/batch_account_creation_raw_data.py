class BatchAccountCreationRawData(object):
    raw_data = None
    send_email = None

    def __init__(self, raw_data=None, send_email=None):
        self.raw_data = raw_data
        self.send_email = send_email
