from django.conf import settings

from app.service.send_email_service import SendEmailService

from action_base import ActionBase


class ActionPrintToConsole(ActionBase):
    def execute(self, action_data):
        print '###### Start ######'
        print action_data
        print '###### End ######'
