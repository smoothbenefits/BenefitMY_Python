from django.conf import settings
from app.models.employee_profile import EmployeeProfile
from app.serializers.employee_profile_profile import EmployeeProfileWithNameSerializer

''' Provides service to handle hash and unhash of keys
'''
class EmployeePinService(object):

    def _get_employee_profile_by_id(self, id):
        try:
            return EmployeeProfile.objects.get(pk=id)
        except EmployeeProfile.DoesNotExist:
            raise Http404

    def get_company_wide_unique_pin(self, company_id, user_id):
        return '{0:02d}{0:04d}'.format(company_id, user_id)
