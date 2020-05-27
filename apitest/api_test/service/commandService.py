import re
import traceback
import logging
from api_test.command.common import *
from api_test.command.control import *
from api_test.service.runService import *
from api_test.service.apiService import ApiService

class CommandService:
    @staticmethod
    def run_command(type, name, value, description, context):
        if type=="common":
            command_class=CommonCommand
        if type=="control":
            command_class=ControlCommand
        method=getattr(command_class,name)
        command={"value":json.loads(value),"result":context["result"],"params":context["value"],"context":context}
        try:
            method(command)
        except (ExecutionCheckException,ExecutionFailException) as e:
            raise e
        except (LoopContinueException,LoopBreakException) as e:
            raise e
        return command["result"]["message"]

    @staticmethod
    def get_all_commands():
        command_list=[]
        command_list.extend(CommandService.get_commands(CommonCommand,"common"))
        command_list.extend(CommandService.get_commands(ControlCommand,"control"))
        return command_list

    @staticmethod
    def get_commands(command_class,command_type):
        command_list=[]
        for key in command_class.__dict__.keys():
            if not key.startswith("__") and not key.startswith("_"):
                method=getattr(command_class,key)
                doc=json.loads(method.__doc__)
                command={"name":key,"type":command_type,"desc":doc["desc"],"alias":doc["alias"],"value":json.dumps(doc["valueDesc"],ensure_ascii=False),"actionId":0}
                if "pattern" in doc:
                    command["pattern"]=doc["pattern"]
                command_list.append(command)
        return command_list

    @staticmethod
    def get_command(line,projectId=None):
        api_pattern="执行接口(?P<name>.*),使用参数(?P<params>.*)"
        match=re.search(api_pattern,line)
        try:
            if match:
                api_name=match.group("name")
                api_params=match.group("params")
                api=ApiService.get_api_by_name(projectId,api_name)
                api_command=None
                if api:
                    api_command={"name":api_name,"type":"api","actionId":api.id,"alias":"","value":api_params,"desc":api.description}
                else:
                    api_command={"name":api_name,"type":"api","actionId":0,"alias":"","value":api_params,"desc":""}
                return api_command
            command_list=[]
            command_list.extend(CommandService.get_commands(CommonCommand,"common"))
            for command in command_list:
                match=re.search(command["pattern"],line)
                if match:
                    valueMap=json.loads(command["value"])
                    for key in valueMap:
                        valueMap[key]=match.group(key)
                    command["value"]=json.dumps(valueMap)
                    return command
        except Exception as e:
            # logging.error(traceback.format_exc())
            raise e

class Command(object):
    name = ""
    value = {}
    result = {}
    desc = ""
    error = ""
    context = {}

    def __init__(self, name="", value={}, result={}, desc="", context={}):
        self.name = name
        self.value = value
        self.result = result
        self.desc = desc
        self.context = context
