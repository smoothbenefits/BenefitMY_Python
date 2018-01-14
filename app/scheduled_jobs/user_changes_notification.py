from django_cron import CronJobBase, Schedule
from django.conf import settings

from app.service.data_modification_service import DataModificationService

''' Cron class required by the Django-cron to perform the scheduled task
    of sending notification emails about user made changes.
'''
class UserChangeNotifications(CronJobBase):

    # set schedule to every 1 minute, to hand over real schedule
    # controlling to the external trigger (e.g. cron tab, scheduled task)
    schedule = Schedule(run_every_mins=1)
    code = 'app.EmployeeDataChangeNotifications'    # a unique code

    # For now, notify brokers and HRs with the same schedule.
    # This could be easily separated by coming up with a separate
    # cron job class.
    def do(self):
        mod_service = DataModificationService()

        # Notify brokers
        mod_service.employee_modifications_notify_all_brokers(settings.DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES)
