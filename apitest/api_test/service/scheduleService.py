from io import StringIO
from apscheduler.scheduler import Scheduler
from django.conf import settings

schedudler = Scheduler(daemonic = False)

if settings.SCHEDULE_START:
    schedudler.start()

def startSchedule():
    schedudler.start()

def addScheduler(jobname, crontab, jobfunc, jobfuncparamslist):
    minute,hour,day,month,dayofweek = tuple(crontab.strip().split(" "))
    schedudler.add_cron_job(jobfunc, minute=minute, hour=hour, day=day, month=month, day_of_week=dayofweek, 
        name=jobname, args=jobfuncparamslist)

def removeScheduler(jobname):
    try:
        jobs=schedudler.get_jobs()
        for job in jobs:
            if job.name==jobname:
                schedudler.unschedule_job(job)
    except:
        pass

def listSchedulers():
    # jbs = schedudler.get_jobs()
    s = StringIO()
    schedudler.print_jobs(out=s)
    s.seek(0)
    jl = s.readlines()
    s.close()
    return jl


