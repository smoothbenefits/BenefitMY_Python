from django_cron import CronJobBase, Schedule

from app.service.system_tasks.system_job.system_job_service import \
    SystemJobService


''' Cron class required by the Django-cron to perform various types
    of system jobs
'''
class SystemJobs(CronJobBase):

    # set schedule to every 1 minute, to hand over real schedule
    # controlling to the external trigger (e.g. cron tab, scheduled task)
    schedule = Schedule(run_every_mins=1)
    code = 'app.SystemJobs'    # a unique code

    def do(self):
        service = SystemJobService()
        service.execute()
