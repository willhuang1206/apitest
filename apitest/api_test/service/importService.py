import logging
import threading
import time
import requests
import traceback
from django.conf import settings
from datetime import datetime
from api_test.service.apiService import ApiService
from api_test.service.automationService import AutomationService
from api_test.models import AutomationResult
from api_test.common.confighttp import run_http
from api_test.common.paramUtil import ParamUtil
from api_test.common.jsonUtil import json
from api_test.common.exception import *
from api_test.common.common import record_dynamic

logger = logging.getLogger(__name__)

class ImportApiThread (threading.Thread):
    def __init__(self, apiInfoList,projectId,userId,toGroupName):
        threading.Thread.__init__(self)
        self.apiInfoList = apiInfoList
        self.projectId=projectId
        self.userId=userId
        self.toGroupName=toGroupName

    def run(self):
        try:
            start = time.clock()
            for apiInfo in self.apiInfoList:
                if "id" in apiInfo:
                    ApiService.updateApi(apiInfo)
                else:
                    ApiService.addApi(apiInfo)
            duration = int(time.clock()-start)
            print("导入%s分组共%s个接口,耗时%s秒!" % (self.toGroupName,len(self.apiInfoList),duration))
            record_dynamic(project=self.projectId,
                       _type="导入", operationObject="接口", user=self.userId,
                       data="导入%s分组共%s个接口,耗时%s秒!" % (self.toGroupName,len(self.apiInfoList),duration))
        except:
            logging.error(traceback.format_exc())

class ImportAutomationThread (threading.Thread):
    def __init__(self, automationList,projectId,userId,toGroupName):
        threading.Thread.__init__(self)
        self.automationList = automationList
        self.projectId=projectId
        self.userId=userId
        self.toGroupName=toGroupName

    def run(self):
        try:
            start = time.clock()
            for automation in self.automationList:
                AutomationService.addAutomation(automation)
            duration = int(time.clock()-start)
            print("导入%s分组共%s个自动化用例,耗时%s秒!" % (self.toGroupName,len(self.automationList),duration))
            record_dynamic(project=self.projectId,
                       _type="导入", operationObject="自动化", user=self.userId,
                       data="导入%s分组共%s个自动化用例,耗时%s秒!" % (self.toGroupName,len(self.automationList),duration))
        except:
            logging.error(traceback.format_exc())

def import_api(apiInfoList,projectId,userId,toGroupName):
    try:
        thread = ImportApiThread(apiInfoList,projectId,userId,toGroupName)
        thread.start()
    except:
        logging.error(traceback.format_exc())

def import_automation(automationList,projectId,userId,toGroupName):
    try:
        thread = ImportAutomationThread(automationList,projectId,userId,toGroupName)
        thread.start()
    except:
        logging.error(traceback.format_exc())
