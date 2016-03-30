from ...trigger_base import TriggerBase


class TriggerTimeoffAccrual(TriggerBase):
    def __init__(self):
        super(TriggerTimeoffAccrual, self).__init__()

    def _examine_condition(self):
        # For now, this just rely on the outer (cron job)
        # schedule 
        return True
