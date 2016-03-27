from django_cron import CronJobBase, Schedule

from app.service.system_tasks.notification.notification_service import \
    NotificationService


''' Cron class required by the Django-cron to perform the scheduled task
    of sending various notifications
'''
class SystemNotifications(CronJobBase):

    # set schedule to every 1 minute, to hand over real schedule
    # controlling to the external trigger (e.g. cron tab, scheduled task)
    schedule = Schedule(run_every_mins=1)
    code = 'app.SystemNotifications'    # a unique code

    def do(self):
        service = NotificationService()
        service.execute()
