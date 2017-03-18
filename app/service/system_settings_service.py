from django.contrib.auth import get_user_model

from app.models.system.system_setting import SystemSetting

User = get_user_model()

# List of tracked setting names
SYSTEM_SETTING_CPAPIAUTHTOKEN = 'CpApiAuthToken'
SYSTEM_SETTING_CPAPIBASEURI = 'CpApiBaseUri'
SYSTEM_SETTING_CPAPIEMPLOYEEROUTE = 'CpApiEmployeeRoute'


class SystemSettingsService(object):

    def get_setting_value_by_name(self, setting_name):
        setting_records = SystemSetting.objects.filter(name=setting_name)
        if (len(setting_records) > 0):
            return setting_records[0].value

        return None
