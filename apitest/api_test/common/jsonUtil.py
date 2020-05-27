import logging
import jsonpath
import json as json2
import datetime
import re

logger = logging.getLogger(__name__)


class json:
    @staticmethod
    def get_value(str, path,index=0):
        if not path.startswith("$."):
            path = "$." + path
        value=jsonpath.jsonpath(str, path)
        if value:
            return value[index]
        else:
            raise Exception("不存在%s元素!" % (path))

    @staticmethod
    def get_values(str, path):
        if not path.startswith("$."):
            path = "$." + path
        value=jsonpath.jsonpath(str, path)
        return value

    @staticmethod
    def get_array(str, path):
        if not path.startswith("$."):
            path = "$." + path
        return jsonpath.jsonpath(str, path)

    @staticmethod
    def loads(json):
        try:
            return json2.loads(json,strict=False)
        except Exception as e:
            raise e

    @staticmethod
    def loads2(json):
        try:
            return json2.loads(json,strict=False)
        except:
            return json

    @staticmethod
    def dumps(str,ensure_ascii=False):
        return json2.dumps(str,cls=DateEncoder,ensure_ascii=ensure_ascii)

    @staticmethod
    def is_json(str):
        try:
            json2.loads(str,strict=False)
        except Exception as e:
            return False
        return True

    @staticmethod
    def get_type(data):
        try:
            if isinstance(data, dict):
                return "Object"
            elif isinstance(data, list):
                return "Array"
            elif isinstance(data, int):
                return "Int"
            elif isinstance(data, float):
                return "Int"
            elif data is None or data=="null":
                return None
            else:
                return "String"
        except:
            return "String"

    @staticmethod
    def assertMatch(actualStr,expectStr,locator=""):
        try:
            if not actualStr:
                return
            if isinstance(actualStr,str):
                actualJson=json.loads2(actualStr)
            else:
                actualJson=actualStr
            if isinstance(expectStr,str):
                expectJson=json.loads2(expectStr)
            else:
                expectJson=expectStr
            if isinstance(expectJson,list):
                if len(actualJson)<len(expectJson):
                    raise Exception("%s长度%s不符合预期%s" % (locator,len(actualJson),len(expectJson)))
                elif len(expectJson)<=1:
                    for i,actual in enumerate(actualJson):
                        json.assertMatch(actual,expectJson[0],locator)
                else:
                    if len(actualJson)!=len(expectJson):
                        raise Exception("%s长度%s不符合预期%s" % (locator,len(actualJson),len(expectJson)))
                    for i,expect in enumerate(expectJson):
                        json.assertMatch(actualJson[i],expect,"%s[%s]" % (locator,str(i)))
            elif isinstance(expectJson,dict):
                if isinstance(actualJson,list):
                    raise Exception("%s类型list不符合预期" % locator)
                else:
                    for key in expectJson:
                        if not key in actualJson:
                            raise Exception("%s没有预期的属性%s" % (locator,key))
                        currentLocator="%s.%s" % (locator,key) if locator else key
                        if isinstance(expectJson[key],dict):
                            json.assertMatch(actualJson[key],expectJson[key],currentLocator)
                        elif isinstance(expectJson[key],list):
                            json.assertMatch(actualJson[key],expectJson[key],currentLocator)
                        elif actualJson[key]!=expectJson[key] and not re.fullmatch(expectJson[key],actualJson[key]):
                            raise Exception("%s实际值%s不符合预期%s" % (currentLocator,actualJson[key],expectJson[key]))
            else:
                if actualJson!=expectJson and not re.fullmatch(expectJson,actualJson):
                    raise Exception("%s实际值%s不符合预期%s" % (locator,actualJson,expectJson))
        except Exception as e:
            raise Exception(e)

class DateEncoder(json2.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json2.JSONEncoder.default(self, obj)