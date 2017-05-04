class AwsMessageQueueConfig(object):
    def __init__(self):
        # For documentation of these SQS attributes
        # see the official SQS documentation
        # http://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html
        
        # In seconds
        self.DelaySeconds = None

        # In bytes
        self.MaximumMessageSize = None

        # In seconds
        self.MessageRetentionPeriod = None

        # In seconds 
        self.ReceiveMessageWaitTimeSeconds = None

        # In seconds
        self.VisibilityTimeout = None

    def to_dict(self):
        return {k: str(v) for k, v in self.__dict__.iteritems() if v is not None}
