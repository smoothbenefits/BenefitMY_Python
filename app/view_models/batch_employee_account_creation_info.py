from app.view_models.view_model_base import ViewModelBase

class BatchEmployeeAccountCreationInfo(ViewModelBase):
    account_creation_info_list = None

    def __init__(self, account_creation_info_list=None):
        self.account_creation_info_list = account_creation_info_list

    def all_accounts_valid(self):
        if (self.account_creation_info_list is not None):
            for account_info in self.account_creation_info_list:
                if (not account_info.is_valid()):
                    return False

        return True
