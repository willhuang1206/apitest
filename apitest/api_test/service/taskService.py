import logging
import threading
import traceback
import ast
from datetime import datetime
from api_test.service.runService import RunService
from api_test.service.reportService import ReportService
from api_test.service import scheduleService
from api_test.models import AutomationTask
from api_test.common.paramUtil import ParamUtil
from api_test.common.jsonUtil import json
from api_test.models import ProjectConfig

class RunTaskThread (threading.Thread):
    def __init__(self, task, context):
        threading.Thread.__init__(self)
        self.task = task
        self.context=context

    def run(self):
        logging.info("Run task {taskname} at {runtime}".format(taskname=self.task.name,runtime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')))
        try:
            trace=datetime.now().strftime('%Y%m%d%H%M%S%f')
            paramMap=json.loads(self.task.params)
            env = ProjectConfig.objects.filter(project=self.task.project.id,name=self.task.env,type="env").order_by("-id")[0]
            envMap=json.loads(env.value)
            env=envMap["env"] if "env" in envMap else ""
            self.context.update({"trace":trace,"value":paramMap,"env":env,"envMap":envMap})
            thread=RunService.run_taskautomations(self.task,self.context)
            thread.join()
            result=thread.result
            if self.task.sendEmail:
                emails=self.task.emails if isinstance(self.task.emails,list) else ast.literal_eval(self.task.emails)
                ReportService().sendTaskReport(self.task,result,emails)
        except:
            logging.error(traceback.format_exc())
        logging.info("Complete task {taskname} at {runtime}".format(taskname=self.task.name,runtime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')))


class TaskService():

    @staticmethod
    def start_task(task):
        logging.info("Start task {taskname} on {crontab}".format(taskname=task.name,crontab=task.crontab))
        context={"project":task.project.id,"result":{},"details":[],"status":"RUNNING","user": 1}
        scheduleService.removeScheduler(task.name)
        scheduleService.addScheduler(task.name, task.crontab, TaskService.run_task,[task,context])

    @staticmethod
    def stop_task(task):
        logging.info("Stop task {taskname}".format(taskname=task.name))
        scheduleService.removeScheduler(task.name)

    @staticmethod
    def run_task(task,context):
        thread = RunTaskThread(task,context)
        thread.start()

    @staticmethod
    def reload_tasks():
        tasks=AutomationTask.objects.filter(status=True).order_by("id")
        for task in tasks:
            TaskService.start_task(task)

TaskService.reload_tasks()