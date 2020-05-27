import logging
import re
import traceback
from api_test.common.jsonUtil import json

logger = logging.getLogger(__name__)


class ParamUtil:
    @staticmethod
    def replaceMap(valueMap,paramMap):
        for key in paramMap.keys():
            # if key in valueMap.keys():
            #     valueMap[key]=paramMap[key]
            # if key.startswith('env'):
            valueMap[key]=paramMap[key]
        return valueMap

    @staticmethod
    def replaceEnvMap(valueMap,paramMap):
        for key in paramMap.keys():
            if key.startswith('env'):
                valueMap[key]=paramMap[key]
        return valueMap

    @staticmethod
    def replaceParam(value,paramMap):
        value=ParamUtil.replace(value,paramMap,start="\$\(",end="\)")
        value=ParamUtil.replace(value,paramMap,start="\$\{",end="}")
        value=ParamUtil.replaceEval(value)
        return value

    @staticmethod
    def replaceResult(value,result):
        start="\$\{"
        end="}"
        it = re.finditer(r"%s(.*?)%s" % (start,end),value)
        for match in it:
            for group in match.groups():
                paramValue=str(json.get_value(result,group))
                value=re.sub(r"%s%s%s" % (start,group,end), paramValue, value)
        return value

    @staticmethod
    def replaceEval(value):
        start='##'
        end='##'
        it = re.finditer(r"%s(.*?)%s" % (start,end),value)
        for match in it:
            for group in match.groups():
                paramValue="%s%s%s" % (start,group,end)
                try:
                    paramValue=str(eval(group))
                except:
                    pass
                value=value.replace("%s%s%s" % (start,group,end),paramValue)
                #value=re.sub(r"%s%s%s" % (start,group,end), paramValue, value)
        return value

    @staticmethod
    def replace(value,paramMap,start="\$\{",end="}"):
        it = re.finditer(r"%s(.*?)%s" % (start,end),value)

        try:
            for match in it:
                for group in match.groups():
                    groups=group.split(",")
                    replaceValue=groups[1] if len(groups)>1 else None
                    index0=groups[0].find('.')
                    index1=groups[0].find('[')
                    index=-1 if index0<0 and index1<0 else index0 if index0>=0 and index1<0 else index1 if index0<0 and index1>=0 else min(index0,index1)
                    if index<0:
                        if groups[0] in paramMap:
                            replaceValue=str(paramMap[groups[0]])
                    else:
                        paramName=groups[0][0:index]
                        paramLocator=groups[0][index:]
                        paramLocator=paramLocator[1:] if paramLocator[0]=='.' else paramLocator
                        if paramName in paramMap:
                            paramValue=json.get_value(paramMap[paramName],paramLocator)
                            if isinstance(paramValue,(dict,list)):
                                replaceValue=paramValue
                            elif isinstance(paramValue,(str,int,float)):
                                replaceValue=str(paramValue)
                            elif paramValue is None:
                                replaceValue="null"
                            else:
                                replaceValue=paramValue
                            # replaceValue=str(paramValue) if not isinstance(paramValue,(dict,list)) else paramValue
                    if replaceValue is not None:
                        group=group.replace("[","\[").replace("]","\]")
                        value=re.sub(r"%s%s%s" % (start,group,end), replaceValue, value)
                        # value=value.replace("%s%s%s" % (start,group,end),replaceValue)
            return value
        except Exception as e:
            logging.error(traceback.format_exc())
