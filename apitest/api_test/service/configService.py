import logging
import traceback
from django.db import transaction,connections
from django.conf import settings
from api_test.common.jsonUtil import json
from api_test.models import GlobalConfig,ProjectConfig

logger = logging.getLogger(__name__)

def getConfigValueByName(name,default=None):
    try:
        configValue=default
        config=GlobalConfig.objects.filter(type="config",name=name,status=True)
        if len(config)>0:
            configValue=config[0].value
    finally:
        return configValue

def getProjectConfigValueByName(projectId,name,default=None):
    try:
        configValue=default
        config=ProjectConfig.objects.filter(project=projectId,name=name,type="config",status=True)
        if len(config)>0:
            configValue=config[0].value
    finally:
        return configValue

def getDataMap(projectId):
    try:
        dataMap={}
        datas=ProjectConfig.objects.filter(project=projectId,type="data",status=True)
        if len(datas)>0:
            for data in datas:
                try:
                    dataMap[data.name]=json.loads(data.value)
                except:
                    dataMap[data.name]=data.value
    finally:
        return dataMap