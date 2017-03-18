from django.contrib.auth import get_user_model

from app.models.system.system_setting import SystemSetting

User = get_user_model()

# List of tracked setting names
SYSTEM_SETTING_CPAPIAUTHTOKEN = 'CpApiAuthToken'
SYSTEM_SETTING_CPAPIBASEURI = 'CpApiBaseUri'
SYSTEM_SETTING_CPAPIEMPLOYEEROUTE = 'CpApiEmployeeRoute'


class SystemSettingsService(object):

    def get_setting_value_by_name(self, setting_name):
        try:
            setting_record = SystemSetting.objects.get(name=setting_name)
            return setting_record.value
        except SystemSetting.DoesNotExist:
            return None
