class BatchAccountCreationRawData:
    raw_data_list = None
    send_email = None

    def __init__(self, raw_data_list=None, send_email=None):
        self.raw_data_list = raw_data_list
        self.send_email = send_email
