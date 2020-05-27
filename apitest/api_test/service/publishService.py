import logging
import threading
import ast
import traceback
import time
from datetime import datetime
from api_test.service.runService import RunService
from api_test.service.reportService import ReportService
from api_test.service.configService import getProjectConfigValueByName
from api_test.service import scheduleService
from api_test.models import AutomationTask
from api_test.common.paramUtil import ParamUtil
from api_test.common.jsonUtil import json
from api_test.models import ProjectConfig,Automation

class RunPublishTestThread (threading.Thread):
    def __init__(self, publish, id,context):
        threading.Thread.__init__(self)
        self.publish = publish
        self.id = id
        self.context = context
        self.result={}

    def run(self):
        publishName="{name}{env}环境上线单{id}".format(name=self.publish.name,env=self.publish.env,id=self.id)
        publishTestWaitTime=int(getProjectConfigValueByName(self.publish.project.id,"PublishTestWaitTime",0))
        if publishTestWaitTime>0:
            logging.info("Wait {waitTime} seconds before publish test {publish}".format(waitTime=publishTestWaitTime,publish=publishName))
            time.sleep(publishTestWaitTime)
        logging.info("Run publish test {publish} at {runtime}".format(publish=publishName,runtime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')))
        try:
            automations=Automation.objects.filter(id__in=ast.literal_eval(self.publish.automations))
            if len(automations)>0:
                thread=RunService.run_automation_publish(self.publish,self.id,automations,[],self.context)
                thread.join()
                self.result=thread.result
                if self.publish.sendEmail:
                    emails=self.publish.emails if isinstance(self.publish.emails,list) else ast.literal_eval(self.publish.emails)
                    self.publish.name=publishName
                    ReportService().sendTaskReport(self.publish,self.result,emails)
        except:
            logging.error(traceback.format_exc())
        logging.info("Complete publish test {publish} at {runtime}".format(publish=publishName,runtime=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')))


class PublishService():

    @staticmethod
    def run_test(publish,id,context):
        thread = RunPublishTestThread(publish,id,context)
        thread.start()
        return thread.result