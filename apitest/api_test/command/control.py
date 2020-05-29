from api_test.common.exception import *
from api_test.service.runService import RunService
from api_test.common.jsonUtil import json
from api_test.common.paramUtil import ParamUtil
import re
import time
import pymysql
import traceback

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class ControlCommand:
    _evals={}

    @staticmethod
    def FOR(command):
        """
        {"desc":"循环以下步骤指定次数，循环的index存放在for_index变量","alias":"for","valueDesc":{"count":"循环次数"},"pattern":"循环次数(?P<count>.*)"}
        """
        try:
            valueMap = command["value"]
            resultMap = command["result"]
            context=command["context"]
            count=int(valueMap["count"])
            context["control"]["forFlag"]=True
            context["control"]["forCount"]=count
            context["control"]["forSteps"]=[]
            resultMap["message"]="for(%s)" % count
        except Exception as e:
            raise ExecutionFailException(e)

    @staticmethod
    def END_FOR(command):
        """
        {"desc":"结束for循环语句","alias":"end for","valueDesc":{},"pattern":"结束次数循环"}
        """
        try:
            resultMap = command["result"]
            context=command["context"]
            if context["control"]["forFlag"] and context["control"]["forCount"]>0:
                for index in range(context["control"]["forCount"]):
                    context["value"]["for_index"]=index
                    try:
                        controlContext=context["control"]
                        RunService.run_steps(context["control"]["forSteps"],context)
                    except LoopContinueException as e:
                        continue
                    except LoopBreakException as e:
                        break
                    except Exception as e:
                        traceback.print_exc()
                        raise ExecutionFailException(e)
                    finally:
                        context["control"]=controlContext
            context["control"]["forFlag"]=False
            context["control"]["forCount"]=0
            context["control"]["forSteps"]=[]
            resultMap["message"]="end for"
        except Exception as e:
            raise ExecutionFailException(e)

    @staticmethod
    def WHILE(command):
        """
        {"desc":"如果条件为真则循环以下步骤","alias":"while","valueDesc":{"eval":"条件判断语句"},"pattern":"循环条件(?P<eval>.*)"}
        """
        try:
            valueMap = command["value"]
            resultMap = command["result"]
            context=command["context"]
            evalStr=valueMap["eval"]
            context["control"]["whileFlag"]=True
            context["control"]["whileEval"]=evalStr
            context["control"]["whileSteps"]=[]
            resultMap["message"]="while(%s)" % evalStr
        except Exception as e:
            raise ExecutionFailException(e)

    @staticmethod
    def END_WHILE(command):
        """
        {"desc":"结束条件循环语句","alias":"end while","valueDesc":{},"pattern":"结束条件循环"}
        """
        try:
            resultMap = command["result"]
            context=command["context"]
            while context["control"]["whileFlag"] and eval(ParamUtil.replaceParam(context["control"]["whileEval"],context["value"])):
                try:
                    controlContext=context["control"]
                    RunService.run_steps(context["control"]["whileSteps"],context)
                except LoopContinueException as e:
                    continue
                except LoopBreakException as e:
                    break
                except Exception as e:
                    raise ExecutionFailException(e)
                finally:
                    context["control"]=controlContext
            context["control"]["whileFlag"]=False
            context["control"]["whileSteps"]=[]
            resultMap["message"]="end while"
        except Exception as e:
            raise ExecutionFailException(e)

    @staticmethod
    def LOOP(command):
        """
        {"desc":"根据指定的数组循环","alias":"loop","valueDesc":{"array":"json格式循环数组"},"pattern":"循环数组(?P<array>.*)"}
        """
        try:
            valueMap = command["value"]
            resultMap = command["result"]
            context=command["context"]
            array=json.loads(ParamUtil.replaceParam(valueMap["array"],context["value"]).replace("'","\"").replace("None","null"))
            context["control"]["loopFlag"]=True
            context["control"]["loopArray"]=array
            context["control"]["loopSteps"]=[]
            resultMap["message"]="loop(%s)" % array
        except Exception as e:
            raise ExecutionFailException(e)

    @staticmethod
    def END_LOOP(command):
        """
        {"desc":"结束数组循环","alias":"end loop","valueDesc":{},"pattern":"结束数组循环"}
        """
        try:
            resultMap = command["result"]
            context=command["context"]
            currentValueMap={}
            currentValueMap.update(context["value"])
            for loopValue in context["control"]["loopArray"]:
                currentValueMap.update(loopValue)
                try:
                    controlContext=context["control"]
                    valueMap=context["value"]
                    context["value"]=currentValueMap
                    RunService.run_steps(context["control"]["loopSteps"],context)
                except LoopContinueException as e:
                    continue
                except LoopBreakException as e:
                    break
                except Exception as e:
                    raise ExecutionFailException(e)
                finally:
                    context["control"]=controlContext
                    context["value"]=valueMap
            context["control"]["loopFlag"]=False
            context["control"]["loopSteps"]=[]
            resultMap["message"]="end loop"
        except Exception as e:
            raise ExecutionFailException(e)

    @staticmethod
    def CONTINUE(command):
        """
        {"desc":"跳过当前循环剩余步骤","alias":"continue","valueDesc":{},"pattern":"继续"}
        """
        raise LoopContinueException()

    @staticmethod
    def BREAK(command):
        """
        {"desc":"跳出当前循环","alias":"break","valueDesc":{},"pattern":"退出"}
        """
        raise LoopBreakException()

    @staticmethod
    def IF(command):
        """
        {"desc":"如果条件语句为真，执行后面的步骤，否则不执行","alias":"if","valueDesc":{"eval":"条件判断语句"},"pattern":"如果(?P<eval>.*)"}
        """
        try:
            valueMap = command["value"]
            resultMap = command["result"]
            context=command["context"]
            evalStr=valueMap["eval"]
            context["control"]["ifEval"]=evalStr
            context["control"]["ifFlag"]=True
            evalStr=ParamUtil.replaceParam(evalStr,context["value"])
            context["control"]["ifResult"]=eval(evalStr)
            resultMap["message"]="if(%s)" % evalStr
        except Exception as e:
            raise ExecutionFailException(e)

    @staticmethod
    def ELSE(command):
        """
        {"desc":"如果条件语句不为真，执行后面的步骤，否则不执行","alias":"else","valueDesc":{},"pattern":"否则"}
        """
        try:
            resultMap = command["result"]
            context=command["context"]
            context["control"]["ifResult"]=not context["control"]["ifResult"]
            resultMap["message"]="else"
        except Exception as e:
            raise ExecutionFailException(e)

    @staticmethod
    def END_IF(command):
        """
        {"desc":"结束条件判断语句","alias":"end if","valueDesc":{},"pattern":"结束条件"}
        """
        try:
            resultMap = command["result"]
            context=command["context"]
            context["control"]["ifEval"]=None
            context["control"]["ifFlag"]=False
            context["control"]["ifResult"]=None
            resultMap["message"]="end if"
        except Exception as e:
            raise ExecutionFailException(e)