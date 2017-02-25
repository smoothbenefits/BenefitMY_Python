from .event_base import EventBase


class TestEvent(EventBase):
    def __init__(self, product_id, product_name):
        super(TestEvent, self).__init__()
        self.product_id = product_id
        self.product_name = product_name
