from django_cron import CronJobBase, Schedule
from django.conf import settings

from app.service.data_modification_service import DataModificationService

''' Cron class required by the Django-cron to perform the scheduled task
    of sending notification emails about user made changes.
'''
class UserChangeNotifications(CronJobBase):

    #schedule = Schedule(run_at_times=['06:02', '06:08', '06:12'])
    schedule = Schedule(run_every_mins=settings.DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES) # Every 24 hours
    code = 'app.EmployeeDataChangeNotifications'    # a unique code

    # For now, notify brokers and HRs with the same schedule. 
    # This could be easily separated by coming up with a separate
    # cron job class.
    def do(self):
        mod_service = DataModificationService()

        # Notify employers
        mod_service.employee_modifications_notify_employer_for_all_companies(settings.DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES)

        # Notify brokers
        mod_service.employee_modifications_notify_all_brokers(settings.DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES)

