from action_base import ActionBase


class ActionPrintToConsole(ActionBase):
    def execute(self, action_data):
        print '###### Start ######'
        print action_data
        print '###### End ######'
