import logging
import traceback
from django.db import transaction,connections
from django.conf import settings
from api_test.common.jsonUtil import json
from api_test.models import ApiInfo

try:
    connection = connections['autotest']
    connection.check_same_thread=False
    cursor=connection.cursor()
except:
    pass

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getApiDomainList():
    try:
        domains=[]
        sql="select DISTINCT domain as id,domain as label from ah_api where domain is not null"
        cursor.execute(sql)
        domains = dictfetchall(cursor)
    except:
        logging.error(traceback.format_exc())
    finally:
        return domains

def getActionDomainList():
    try:
        domains=[]
        sql="select DISTINCT domain as id,domain as label from ah_action where domain is not null"
        cursor.execute(sql)
        domains = dictfetchall(cursor)
    except:
        logging.error(traceback.format_exc())
    finally:
        return domains

def getAutoApis(fromDate,toDate,domain):
    dateWhere="and (created_on between '{fromDate}' and '{toDate}' or updated_on between '{fromDate}' and '{toDate}')".format(fromDate=fromDate,toDate=toDate) if fromDate and toDate else ""
    sql="select * from ah_api where domain='{domain}' {dateWhere} and status=0".format(domain=domain,dateWhere=dateWhere)
    cursor.execute(sql)
    apis = dictfetchall(cursor)
    return apis

def getAutoAutomations(fromDate,toDate,domain):
    dateWhere="and (created_on between '{fromDate}' and '{toDate}' or updated_on between '{fromDate}' and '{toDate}')".format(fromDate=fromDate,toDate=toDate) if fromDate and toDate else ""
    sql="select * from ah_action where tag like '%已完成%' and domain='{domain}' and type in ('normal','reuse') {dateWhere} and status=0".format(domain=domain,dateWhere=dateWhere)
    cursor.execute(sql)
    automations = dictfetchall(cursor)
    return automations

def getAutoActionSteps(actionId):
    actionSteps=[]
    try:
        sql="select * from ah_action where id='%s'" % actionId
        cursor.execute(sql)
        action = dictfetchall(cursor)
        if len(action)>0:
            steps=json.loads(action[0]["steps"])
        for step in steps:
            if step["group"]=="ACTION":
                actionSteps.extend(getAutoActionSteps(step["actionId"]))
            elif step["group"]=="API":
                api=ApiInfo.objects.filter(name=step["action"])
                if len(api)>0:
                    currentStep={"type":"api","name":step["action"],"actionId":api[0].id,"params":step["value"],"description":step["description"],"disable":step["disable"]}
                    actionSteps.append(currentStep)
                else:
                    print("导入用例步骤[%s]时,存在不能识别的接口[%s]" % (action[0]["name"],step["action"]))
            elif step["group"] in ["COMMON"]:
                currentStep={"type":step["group"].lower(),"name":step["action"],"actionId":0,"params":step["value"],"description":step["description"],"disable":step["disable"]}
                actionSteps.append(currentStep)
            else:
                print("导入用例[%s]时,存在不能识别的步骤[%s]" % (action[0]["name"],step["action"]))
    except:
        logging.error(traceback.format_exc())
    return actionSteps