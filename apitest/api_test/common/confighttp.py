import django
import sys
import os
import traceback


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apitest.settings")
django.setup()

from api_test.common.jsonUtil import json
import logging
import requests
import simplejson

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。

def run_http(request_type, header, url, request_parameter_type, parameter,cookies=None):
    try:
        if request_type == 'GET':
            code, response_data, header_data = get(header, url, request_parameter_type, parameter,cookies)
        elif request_type == 'POST':
            code, response_data, header_data = post(header, url, request_parameter_type, parameter,cookies)
        elif request_type == 'PUT':
            code, response_data, header_data = put(header, url, request_parameter_type, parameter,cookies)
        elif request_type == 'DELETE':
            code, response_data, header_data = delete(header, url, parameter,cookies)
    except Exception as e:
        code,response_data,header_data=500,str(e),{}
    return code, response_data, header_data


def post(header, address, request_parameter_type, data,cookies):
    """
    post 请求
    :param header:  请求头
    :param address:  host地址
    :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
    :param data: 请求参数
    :return:
    """
    try:
        if request_parameter_type=='application/json':
            try:
                data=json.loads(data)
            except:
                pass
            response = requests.post(url=address, json=data, headers=header, timeout=20,cookies=cookies)
        else:
            if request_parameter_type == 'raw':
                try:
                    data=json.loads(data)
                    response = requests.post(url=address, json=data, headers=header, timeout=20,cookies=cookies)
                except:
                    response = requests.post(url=address, data=data, headers=header, timeout=20,cookies=cookies)
            else:
                response = requests.post(url=address, data=data, headers=header, timeout=20,cookies=cookies)
        if cookies!=None:
            cookies.update(response.cookies)
        try:
            return response.status_code, response.json(), response.headers
        except:
            return response.status_code, response.text, response.headers
    except Exception as e:
        return {}, str(e), {}


def get(header, address, request_parameter_type, data,cookies):
    """
    get 请求
    :param header:  请求头
    :param address:  host地址
    :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
    :param data: 请求参数
    :return:
    """
    try:
        if request_parameter_type == 'raw':
            data = json.dumps(data)
        response = requests.get(url=address, params=data, headers=header, timeout=20,cookies=cookies,allow_redirects=False)
        if cookies!=None:
            cookies.update(response.cookies)
        while response.status_code == 302:
            response = requests.get(url=response.headers["location"],cookies=cookies,allow_redirects=False)
            if cookies!=None:
                cookies.update(response.cookies)
        # if response.status_code == 301:
        #     response = requests.get(url=response.headers["location"],cookies=cookies)
        try:
            return response.status_code, response.json(), response.headers
        except:
            return response.status_code, response.text, response.headers
    except Exception as e:
        return {}, str(e), {}

def put(header, address, request_parameter_type, data,cookies):
    """
    put 请求
    :param header:  请求头
    :param address:  host地址
    :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
    :param data: 请求参数
    :return:
    """
    if request_parameter_type == 'raw':
        data = json.dumps(data)
    response = requests.put(url=address, data=data, headers=header, timeout=20,cookies=cookies)
    if cookies!=None:
        cookies.update(response.cookies)
    try:
        return response.status_code, response.json(), response.headers
    except json.decoder.JSONDecodeError:
        return response.status_code, '', response.headers
    except simplejson.errors.JSONDecodeError:
        return response.status_code, '', response.headers
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        return {}, str(e), {}


def delete(header, address, data,cookies):
    """
    put 请求
    :param header:  请求头
    :param address:  host地址
    :param data: 请求参数
    :return:
    """
    response = requests.delete(url=address, params=data, headers=header,cookies=cookies)
    if cookies!=None:
        cookies.update(response.cookies)
    try:
        return response.status_code, response.json(), response.headers
    except json.decoder.JSONDecodeError:
        return response.status_code, '', response.headers
    except simplejson.errors.JSONDecodeError:
        return response.status_code, '', response.headers
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        return {}, str(e), {}
