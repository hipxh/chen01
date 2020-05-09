import requests
import json
import urllib


# 用于header中带有access_token的情况

# get请求
def getToJson(url, token=None, cookies=None, headers={}, params_obj={}):
    if token is not None:
        headers['Authorization'] = 'Bearer ' + token
    params = urllib.parse.urlencode(params_obj).encode('utf-8')
    response = requests.get(url + "?" + str(params, 'utf-8'), headers=headers,cookies=cookies)
    return to_response(response)

def get(url, token=None, cookies=None,headers={}, params_obj={}):
    if token is not None:
        headers['Authorization'] = 'Bearer ' + token
    params = urllib.parse.urlencode(params_obj).encode('utf-8')
    response = requests.get(url + "?" + str(params, 'utf-8'), headers=headers,cookies=cookies)
    return response


# post请求 入参为application/json这种情况
def postToJson(url, token=None,
         headers={'Content-type': 'application/json;charset=UTF-8', 'Accept': 'application/json, text/plain'},
         params={}):
    if token is not None:
        headers['Authorization'] = 'Bearer ' + token
    response = requests.post(url, data=json.dumps(params),
                             headers=headers)
    return to_response(response)

def post(url, token=None,
         headers={'Content-type': 'application/json;charset=UTF-8', 'Accept': 'application/json, text/plain'},
         params={}):
    if token is not None:
        headers['Authorization'] = 'Bearer ' + token
    response = requests.post(url, data=json.dumps(params),
                             headers=headers)
    return response


# 将get post请求的结果(byte[])转成对象
def to_response(response):
    # 得到的是byte[]
    byte_content = response.content
    # 转成字符串
    content = str(byte_content, 'utf-8')
    # 转成对象
    return json.loads(content)

