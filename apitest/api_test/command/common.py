from api_test.common.exception import *
from api_test.common.jsonUtil import json
from api_test.common.paramUtil import ParamUtil
import re
import time
import pymysql
import traceback
import logging
import paramiko
import requests

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def equals(expect,actual):
    result=False
    try:
        if expect.isnumeric():
            result=float(expect)==float(actual)
        else:
            result=str(expect)==str(actual)
    except:
        pass
    return result

class CommonCommand():
    _evals={}

    @staticmethod
    def assertResultNotEquals(command):
        """
        {"desc":"验证结果不相等","alias":"验证结果不相等","valueDesc":{"expected":"预期不相等的值","locator":"json提取表达式"},"pattern":"验证结果(?P<locator>.*)不是(?P<expected>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        expected = str(valueMap["expected"]).strip()
        locator = valueMap["locator"].strip()
        check=valueMap["check"] if "check" in valueMap.keys() else False

        if not locator or len(locator)==0:
            if equals(expected,resultMap["result"]):
                command["error"]="实际结果是（" + resultMap["result"] + "）与预期一致"
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]="实际返回值为" + resultMap["result"]
        else:
            actual=""
            errorList=[]
            try:
                actual=json.get_value(resultMap["result"],locator)
            except Exception as err:
                logging.error(traceback.format_exc())
                command["error"]=err
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            if equals(expected,actual):
                errorList.append("locator为%s的实际值为%s" % (locator,actual))
            if len(errorList)>0:
                if len(errorList)>1:
                    command["error"]=json.dumps(errorList)
                else:
                    command["error"]=errorList[0]
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]=locator + "的实际值为" + actual

    @staticmethod
    def assertResultEquals(command):
        """
        {"desc":"验证结果相等","alias":"验证结果相等","valueDesc":{"expected":"预期值","locator":"json提取表达式"},"pattern":"验证结果(?P<locator>.*)是(?P<expected>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        expected = str(valueMap["expected"]).strip()
        locator = valueMap["locator"].strip()
        check=valueMap["check"] if "check" in valueMap.keys() else False

        if not locator or len(locator)==0:
            if not equals(expected,resultMap["result"]):
                command["error"]="实际结果是（" + resultMap["result"] + "）与预期不一致"
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]="实际返回值符合预期结果" + expected
        else:
            actual=""
            errorList=[]
            try:
                actual=json.get_value(resultMap["result"],locator)
            except Exception as err:
                command["error"]=err
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            if not equals(expected,actual):
                errorList.append("locator为%s的结果值为%s，不符合预期值%s" % (locator,actual,expected))
            if len(errorList)>0:
                if len(errorList)>1:
                    command["error"]=json.dumps(errorList)
                else:
                    command["error"]=errorList[0]
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]=locator + "的实际值符合预期结果" + expected

    @staticmethod
    def assertResulNotContains(command):
        """
        {"desc":"验证结果不包含","alias":"验证结果不包含","valueDesc":{"expected":"预期值","locator":"json提取表达式"},"pattern":"验证结果(?P<locator>.*)不包含(?P<expected>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        expected = str(valueMap["expected"]).strip()
        locator = valueMap["locator"].strip()
        check=valueMap["check"] if "check" in valueMap.keys() else False

        if not locator or len(locator)==0:
            if expected in resultMap["result"]:
                command["error"]="实际结果包含预期值(" + expected + ")"
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]="实际结果不包含预期值(" + expected + ")"
        else:
            actual=""
            errorList=[]
            try:
                actual=json.get_value(resultMap["result"],locator)
            except Exception as err:
                command["error"]=err
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            if expected in actual:
                errorList.append("locator为%s的结果值为%s，包含预期值%s" % (locator,actual,expected))
            if len(errorList)>0:
                if len(errorList)>1:
                    command["error"]=json.dumps(errorList)
                else:
                    command["error"]=errorList[0]
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]=locator + "的实际值不包含预期值" + expected

    @staticmethod
    def assertResultContains(command):
        """
        {"desc":"验证结果包含","alias":"验证结果包含","valueDesc":{"expected":"预期值","locator":"json提取表达式"},"pattern":"验证结果(?P<locator>.*)包含(?P<expected>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        expected = str(valueMap["expected"]).strip()
        locator = valueMap["locator"].strip()
        check=valueMap["check"] if "check" in valueMap.keys() else False

        if not locator or len(locator)==0:
            if not expected in resultMap["result"]:
                command["error"]="实际结果不包含预期值(" + expected + ")"
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]="实际结果包含预期值(" + expected  + ")"
        else:
            actual=""
            errorList=[]
            try:
                actual=json.get_value(resultMap["result"],locator)
            except Exception as err:
                command["error"]=err
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            if not expected in actual:
                errorList.append("locator为%s的结果值为%s，不包含预期值%s" % (locator,actual,expected))
            if len(errorList)>0:
                if len(errorList)>1:
                    command["error"]=json.dumps(errorList)
                else:
                    command["error"]=errorList[0]
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]=locator + "的实际值包含预期值" + expected

    @staticmethod
    def assertResultNotBlank(command):
        """
        {"desc":"验证结果不为空","alias":"验证结果不为空","valueDesc":{"locator":"json提取表达式"},"pattern":"验证结果(?P<locator>.*)不为空"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        locator = valueMap["locator"].strip()
        check=valueMap["check"] if "check" in valueMap.keys() else False

        if not locator or len(locator)==0:
            if len(resultMap["result"])==0:
                command["error"]="实际结果为空"
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]="实际结果不为空"
        else:
            actual=""
            errorList=[]
            try:
                actual=json.get_value(resultMap["result"],locator)
            except Exception as err:
                logging.error(traceback.format_exc())
                command["error"]=err
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            if not actual or len(actual)==0:
                errorList.append("locator为%s的结果值为空" % (locator))
            if len(errorList)>0:
                if len(errorList)>1:
                    command["error"]=json.dumps(errorList)
                else:
                    command["error"]=errorList[0]
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]="locator为%s的结果值不为空" % (locator)

    @staticmethod
    def assertResultBlank(command):
        """
        {"desc":"验证结果为空","alias":"验证结果为空","valueDesc":{"locator":"json提取表达式"},"pattern":"验证结果(?P<locator>.*)为空"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        locator = valueMap["locator"].strip()
        check=valueMap["check"] if "check" in valueMap.keys() else False

        if not locator or len(locator)==0:
            if len(resultMap["result"])>0:
                command["error"]="实际结果不为空"
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]="实际结果为空"
        else:
            actual=""
            errorList=[]
            try:
                actual=json.get_value(resultMap["result"],locator)
            except Exception as err:
                logging.error(traceback.format_exc())
                command["error"]=err
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            if actual:
                errorList.append("locator为%s的实际值为%s,不为空" % (locator,actual))
            if len(errorList)>0:
                if len(errorList)>1:
                    command["error"]=json.dumps(errorList)
                else:
                    command["error"]=errorList[0]
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]="locator为%s的实际值为空" % (locator)

    @staticmethod
    def assertResultNotTrue(command):
        """
        {"desc":"验证结果不满足表达式","alias":"验证结果不满足表达式","valueDesc":{"eval":"表达式"},"pattern":"验证结果表达式(?P<eval>.*)不为真"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        evalstr = str(valueMap["eval"]).strip()
        evalstr=ParamUtil.replaceResult(evalstr,resultMap["result"])

        if eval(evalstr):
            command["error"]="表达式(%s)为真" % evalstr
            raise ExecutionFailException(command["error"])

        resultMap["message"]="表达式(%s)不为真" % evalstr

    @staticmethod
    def assertResultTrue(command):
        """
        {"desc":"验证结果满足表达式","alias":"验证结果满足表达式","valueDesc":{"eval":"表达式"},"pattern":"验证结果表达式(?P<eval>.*)为真"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        evalstr = str(valueMap["eval"]).strip()
        evalstr=ParamUtil.replaceResult(evalstr,resultMap["result"])

        if not eval(evalstr):
            command["error"]="表达式(%s)不为真" % evalstr
            raise ExecutionFailException(command["error"])

        resultMap["message"]="表达式(%s)为真" % evalstr

    @staticmethod
    def assertNotTrue(command):
        """
        {"desc":"验证表达式不为真","alias":"验证表达式不为真","valueDesc":{"eval":"表达式"},"pattern":"验证表达式(?P<eval>.*)不为真"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        paramMap = command["params"]
        evalstr = str(valueMap["eval"]).strip()
        evalstr=ParamUtil.replaceParam(evalstr,paramMap)

        if eval(evalstr):
            command["error"]="表达式(%s)为真" % evalstr
            raise ExecutionFailException(command["error"])

        resultMap["message"]="表达式(%s)不为真" % evalstr

    @staticmethod
    def assertTrue(command):
        """
        {"desc":"验证表达式为真","alias":"验证表达式为真","valueDesc":{"eval":"表达式"},"pattern":"验证表达式(?P<eval>.*)为真"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        paramMap = command["params"]
        evalstr = str(valueMap["eval"]).strip()
        evalstr=ParamUtil.replaceParam(evalstr,paramMap)

        if not eval(evalstr):
            command["error"]="表达式(%s)不为真" % evalstr
            raise ExecutionFailException(command["error"])

        resultMap["message"]="表达式(%s)为真" % evalstr

    @staticmethod
    def assertResultMatch(command):
        """
        {"desc":"验证结果符合正则表达式","alias":"验证结果符合正则","valueDesc":{"regexp":"表达式","locator":"json提取表达式"},"pattern":"验证结果(?P<locator>.*)匹配(?P<regexp>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        regexp = str(valueMap["regexp"]).strip()
        locator = valueMap["locator"].strip()
        check=valueMap["check"] if "check" in valueMap.keys() else False

        if not locator or len(locator)==0:
            if not re.fullmatch(regexp,resultMap["result"]):
                command["error"]="实际结果是（" + resultMap["result"] + "）与预期不一致"
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]="实际返回值符合预期正则" + regexp
        else:
            actual=""
            errorList=[]
            try:
                actual=json.get_value(resultMap["result"],locator)
            except Exception as err:
                command["error"]=err
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            if not re.fullmatch(regexp,str(actual)):
                errorList.append("locator为%s的结果值为%s，不符合预期正则%s" % (locator,actual,regexp))
            if len(errorList)>0:
                if len(errorList)>1:
                    command["error"]=json.dumps(errorList)
                else:
                    command["error"]=errorList[0]
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            resultMap["message"]=locator + "的实际值符合预期正则" + regexp

    @staticmethod
    def assertResultFormat(command):
        """
        {"desc":"验证结果符合预期json格式","alias":"验证结果格式","valueDesc":{"expected":"预期格式","locator":"json提取表达式"},"pattern":"验证结果(?P<locator>.*)符合(?P<expected>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        expected = valueMap["expected"]
        locator = valueMap["locator"].strip()
        check=valueMap["check"] if "check" in valueMap.keys() else False

        if not locator or len(locator)==0:
                try:
                    json.assertMatch(resultMap["result"],expected)
                    resultMap["message"]="实际值符合预期" + str(expected)
                except Exception as e:
                    command["error"]=str(e)
                    if check:
                        raise ExecutionCheckException(command["error"])
                    else:
                        raise ExecutionFailException(command["error"])
        else:
            actual=""
            errorList=[]
            try:
                actual=json.get_value(resultMap["result"],locator)
            except Exception as err:
                command["error"]=err
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])
            try:
                json.assertMatch(actual,expected,locator)
                resultMap["message"]=locator + "实际值符合预期" + str(expected)
            except Exception as e:
                errorList.append(str(e))
            if len(errorList)>0:
                if len(errorList)>1:
                    command["error"]=json.dumps(errorList)
                else:
                    command["error"]=errorList[0]
                if check:
                    raise ExecutionCheckException(command["error"])
                else:
                    raise ExecutionFailException(command["error"])

    @staticmethod
    def storeGlobalVariable(command):
        """
        {"desc":"保存全局数据","alias":"保存全局数据","valueDesc":{"value":"数据","name":"全局参数名"},"pattern":"保存数据(?P<value>.*)为全局参数(?P<name>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        paramName = valueMap["name"].strip()
        paramValue = valueMap["value"].strip()
        try:
            storedGlobalVariableMap={}
            if "storedGlobalVariable" in resultMap.keys():
                storedGlobalVariableMap=resultMap["storedGlobalVariable"]
            storedGlobalVariableMap[paramName]=paramValue
            resultMap["storedGlobalVariable"]=storedGlobalVariableMap
            resultMap["message"]="保存结果值" + paramValue + "到全局变量" + paramName
        except Exception as e:
            logging.error(traceback.format_exc())
            command["error"]=str(e)
            raise ExecutionFailException(command["error"])

    @staticmethod
    def storeAutomationVariable(command):
        """
        {"desc":"保存数据到用例参数","alias":"保存用例参数","valueDesc":{"value":"数据","name":"用例参数名"},"pattern":"保存数据(?P<value>.*)为用例参数(?P<name>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        paramName = valueMap["name"].strip()
        paramValue = valueMap["value"].strip()
        try:
            storedAutomationVariableMap={}
            if "storedAutomationVariable" in resultMap.keys():
                storedAutomationVariableMap=resultMap["storedAutomationVariable"]
            storedAutomationVariableMap[paramName]=paramValue
            resultMap["storedAutomationVariable"]=storedAutomationVariableMap
            resultMap["message"]="保存数据[" + paramValue + "]到用例参数" + paramName
        except Exception as e:
            logging.error(traceback.format_exc())
            command["error"]=str(e)
            raise ExecutionFailException(command["error"])

    @staticmethod
    def storeVariable(command):
        """
        {"desc":"保存数据","alias":"保存数据","valueDesc":{"value":"数据","name":"参数名"},"pattern":"保存数据(?P<value>.*)为参数(?P<name>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        parm_name = valueMap["name"].strip()
        param_value = valueMap["value"].strip()
        try:
            storedVariableMap={}
            if "storedVariable" in resultMap.keys():
                storedVariableMap=resultMap["storedVariable"]
            storedVariableMap[parm_name]=param_value
            resultMap["storedVariable"]=storedVariableMap
            resultMap["message"]="保存结果值" + param_value + "到变量" + parm_name
        except Exception as e:
            logging.error(traceback.format_exc())
            command["error"]=str(e)
            raise ExecutionFailException(command["error"])

    @staticmethod
    def storeArrayLen(command):
        """
        {"desc":"保存数组长度","alias":"保存数组长度","valueDesc":{"locator":"json路径","name":"参数名"},"pattern":"保存结果数组(?P<locator>.*)长度为参数(?P<name>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        paramName = valueMap["name"].strip()
        locator = valueMap["locator"].strip()
        array=[]
        try:
            array=json.get_array(resultMap["result"],locator)
            if not isinstance(array, list):
               raise ExecutionFailException("实际结果不是数组!")
            length=len(array[0])
            storedVariableMap={}
            if "storedVariable" in resultMap.keys():
                storedVariableMap=resultMap["storedVariable"]
            storedVariableMap[paramName]=length
            resultMap["storedVariable"]=storedVariableMap
            resultMap["message"]="保存%s的数组长度%s到参数%s" % (locator,length,paramName)
        except Exception as e:
            logging.error(traceback.format_exc())
            command["error"]=str(e)
            raise ExecutionFailException(command["error"])

    @staticmethod
    def storeResultByRegex(command):
        """
        {"desc":"通过正则表达式从结果提取值并保存","alias":"保存正则结果","valueDesc":{"regex":"正则表达式","name":"参数名"},"pattern":"保存结果正则(?P<regex>.*)为参数(?P<name>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        paramName = valueMap["name"].strip()
        regex = valueMap["regex"].strip()
        paramValue=""
        try:
            match=re.search(r"%s" % regex,json.dumps(resultMap["result"]))
            if match:
                paramValue=match.group(1)
        except Exception as e:
            logging.error(traceback.format_exc())
            command["error"]=str(e)
            raise ExecutionFailException(command["error"])
        storedVariableMap={}
        if "storedVariable" in resultMap.keys():
            storedVariableMap=resultMap["storedVariable"]
        storedVariableMap[paramName]=paramValue
        resultMap["storedVariable"]=storedVariableMap
        resultMap["message"]="保存结果值" + paramValue + "到变量" + paramName

    @staticmethod
    def storeResultVariable(command):
        """
        {"desc":"保存结果locator到name","alias":"保存结果","valueDesc":{"locator":"json路径","name":"参数名"},"pattern":"保存结果(?P<locator>.*)为参数(?P<name>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        paramName = valueMap["name"].strip()
        locator = valueMap["locator"].strip()
        paramValue=""
        try:
            if not locator or len(locator)==0:
                value=resultMap["result"]
            else:
                value=json.get_value(resultMap["result"],locator)
            if isinstance(value,(dict,list)):
                paramValue=value
            elif isinstance(value,(str,int,float)):
                paramValue=str(value)
            elif value is None:
                paramValue="null"
            else:
                paramValue=value
        except Exception as e:
            logging.error(traceback.format_exc())
            command["error"]=str(e)
            raise ExecutionFailException(command["error"])

        storedVariableMap={}
        if "storedVariable" in resultMap.keys():
            storedVariableMap=resultMap["storedVariable"]
        storedVariableMap[paramName]=paramValue
        resultMap["storedVariable"]=storedVariableMap
        resultMap["message"]="保存结果值" + str(paramValue) + "到变量" + paramName

    @staticmethod
    def sleep(command):
        """
        {"desc":"等待指定时间(秒)","alias":"等待","valueDesc":{"seconds":"等待秒数"},"pattern":"等待(?P<seconds>.*)秒"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        seconds = float(valueMap["seconds"].strip())
        try:
            time.sleep(seconds)
        except Exception as e:
            logging.error(traceback.format_exc())
            command["error"]=str(e)
            raise ExecutionFailException(command["error"])
        resultMap["message"]="等待%s秒" % seconds

    @staticmethod
    def print(command):
        """
        {"desc":"打印数据","alias":"打印数据","valueDesc":{"value":"数据"},"pattern":"输出(?P<value>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        value = valueMap["value"].strip()
        resultMap["message"]=value

    @staticmethod
    def runSql(command):
        """
        {"desc":"执行sql","alias":"执行sql","valueDesc":{"host":"数据库host","port":"3306","database":"数据库","username":"用户名","password":"密码","sql":"sql语句"},"pattern":"使用用户名(?P<username>.*)和密码(?P<password>.*)连接数据库(?P<host>.*):(?P<port>.*)名称为(?P<database>.*)执行(?P<sql>.*)"}
        """

        try:
            valueMap = command["value"]
            resultMap = command["result"]
            host = valueMap["host"].strip()
            port = int(valueMap["port"])
            database = valueMap["database"].strip()
            username = valueMap["username"].strip()
            password = valueMap["password"].strip()
            sql = valueMap["sql"].strip()
            result= ""

            # 打开数据库连接
            db = pymysql.connect(host,username,password,database,port=port,charset='utf8')
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            if sql.startswith("select") or sql.startswith("SELECT"):
                result=dictfetchall(cursor)
            else:
                result=str(cursor.rowcount)
                db.commit()
        except Exception as e:
            # 如果发生错误则回滚
            logging.error(traceback.format_exc())
            try:
                db.rollback()
            except:
                pass
            raise ExecutionFailException(e)
        finally:
            # 关闭数据库连接
            try:
                db.close()
            except:
                pass
        resultMap["result"]=result
        resultMap["message"]=result

    @staticmethod
    def runEval(command):
        """
        {"desc":"执行表达式","alias":"执行表达式","valueDesc":{"eval":"表达式,多行用;分隔","name":"表达式名称"},"pattern":"执行表达式(?P<eval>.*)名称为(?P<name>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        eval_str = valueMap["eval"].strip()
        eval_name = valueMap["name"].strip() if "name" in valueMap else ""

        if eval_str=="" and eval_name!="" and eval_name in CommonCommand._evals:
            eval_str=CommonCommand._evals[eval_name]
        elif eval_str!="" and eval_name!="":
            CommonCommand._evals[eval_name]=eval_str

        try:
            evals=eval_str.split(";")
            for item in evals:
                exec(item,globals(),locals())
            last_eval=evals[len(evals)-1].split("=")
            if len(last_eval)>1:
                eval_param_name=last_eval[0]
                storedVariableMap={}
                if "storedVariable" in resultMap.keys():
                    storedVariableMap=resultMap["storedVariable"]
                eval="storedVariableMap['%s']=%s" % (eval_param_name,eval_param_name)
                exec(eval)
                resultMap["storedVariable"]=storedVariableMap
                resultMap["message"]="保存结果值" + storedVariableMap[eval_param_name] + "到变量" + eval_param_name
            else:
                resultMap["message"]="执行表达式成功"
        except Exception as e:
            logging.error(traceback.format_exc())
            raise ExecutionFailException(e)

    @staticmethod
    def runSSH(command):
        """
        {"desc":"执行ssh语句","alias":"执行ssh","valueDesc":{"host":"服务器host","port":"22","username":"用户名","password":"密码","command":"执行的ssh语句"},"pattern":"使用用户名(?P<username>.*)和密码(?P<password>.*)连接服务器(?P<host>.*):(?P<port>.*)执行(?P<command>.*)"}
        """

        try:
            valueMap = command["value"]
            resultMap = command["result"]
            host = valueMap["host"].strip()
            port = int(valueMap["port"])
            username = valueMap["username"].strip()
            password = valueMap["password"].strip()
            command = valueMap["command"].strip()
            result= ""

            ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            ssh.connect(hostname=host, port=port, username=username, password=password)
            # 执行命令
            stdin, stdout, stderr = ssh.exec_command(command)
            # 获取命令结果
            res,err = stdout.read(),stderr.read()

            result = res if res else err

            logging.info("执行run_ssh返回结果: %s" % result.decode())

        except Exception as e:
            # 如果发生错误则回滚
            logging.error(traceback.format_exc())
            raise ExecutionFailException(e)
        finally:
            ssh.close()

        resultMap["result"]=result.decode()
        resultMap["message"]=result.decode()

    @staticmethod
    def httpGet(command):
        """
        {"desc":"执行http请求Get","alias":"执行Get","valueDesc":{"url":"请求地址"},"pattern":"get请求(?P<url>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        url = valueMap["url"].strip()

        try:
            response = requests.get(url=url)
        except Exception as e:
            logging.error(traceback.format_exc())
            raise ExecutionFailException(e)
        resultMap["result"]=response.text
        resultMap["message"]=response.text

    @staticmethod
    def httpPost(command):
        """
        {"desc":"执行http请求Post","alias":"执行Post","valueDesc":{"url":"请求地址","data":"请求数据"},"pattern":"post请求(?P<url>.*)数据为(?P<data>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        url = valueMap["url"].strip()
        data = valueMap["data"].strip()

        try:
            try:
                data=json.loads(data)
            except:
                pass
            response = requests.post(url=url, json=data)
        except Exception as e:
            logging.error(traceback.format_exc())
            raise ExecutionFailException(e)
        resultMap["result"]=response.text
        resultMap["message"]=response.text

    @staticmethod
    def fail(command):
        """
        {"desc":"执行失败","alias":"执行失败","valueDesc":{"message":"输出的信息"},"pattern":"执行失败提示(?P<message>.*)"}
        """
        valueMap = command["value"]
        resultMap = command["result"]
        message = str(valueMap["message"]).strip()

        raise ExecutionFailException(message)