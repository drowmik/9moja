from django_cron import CronJobBase, Schedule


class FbScrapperCron(CronJobBase):
    """
    tasks here will added in cron
    
    docs: http://django-cron.readthedocs.io/en/latest/installation.html
    
    to run this cron: ./manage.py runcrons "fbs_cron.cron.FbScrapperCron"
    
    cron command
    */5 * * * *
    source /home/<user>/.bashrc &&
    source /<virtual env>/bin/activate &&
    python /<project directory>/manage.py runcrons > /<somewhere for log>/cronjob.log
    """
    
    # RUN_EVERY_MINS = 120  # every 2 hours
    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    RUN_AT_TIMES = ['10:00', '18:00', '2:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    
    code = 'my_app.my_cron_job'  # a unique code
    
    def do(self):
        # cron tasks
        print("ok")
