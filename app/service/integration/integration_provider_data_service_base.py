from django.contrib.auth import get_user_model

User = get_user_model()


class IntegrationProviderDataServiceBase(object):

    def __init__(self):
        pass

    def sync_employee_data_to_remote(self, employee_user_id):
        pass
