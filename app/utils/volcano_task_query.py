import json
import sys
import os
import base64
import datetime
import hashlib
import hmac
import requests
from typing import Optional
from PIL import Image
import io
from app.core.config import settings

method = 'POST'
host = 'visual.volcengineapi.com'
endpoint = 'https://visual.volcengineapi.com'
service = 'cv'


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(key.encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'request')
    return kSigning


def formatQuery(parameters):
    request_parameters_init = ''
    for key in sorted(parameters):
        request_parameters_init += key + '=' + parameters[key] + '&'
    request_parameters = request_parameters_init[:-1]
    return request_parameters


def signV4Request(access_key, secret_key, service, req_query, req_body):
    if access_key is None or secret_key is None:
        print('No access key is available.')
        sys.exit()
    
    t = datetime.datetime.utcnow()
    current_date = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope
    
    canonical_uri = '/'
    canonical_querystring = req_query
    signed_headers = 'content-type;host;x-content-sha256;x-date'
    
    payload_hash = hashlib.sha256(req_body.encode('utf-8')).hexdigest()
    content_type = 'application/json'
    
    canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + host + \
        '\n' + 'x-content-sha256:' + payload_hash + \
        '\n' + 'x-date:' + current_date + '\n'
    
    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + \
        '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
    
    algorithm = 'HMAC-SHA256'
    credential_scope = datestamp + '/' + settings.VOLCANO_REGION + '/' + service + '/' + 'request'
    
    string_to_sign = algorithm + '\n' + current_date + '\n' + credential_scope + '\n' + hashlib.sha256(
        canonical_request.encode('utf-8')).hexdigest()
    
    signing_key = getSignatureKey(secret_key, datestamp, settings.VOLCANO_REGION, service)
    signature = hmac.new(signing_key, (string_to_sign).encode(
        'utf-8'), hashlib.sha256).hexdigest()
    
    authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + \
        credential_scope + ', ' + 'SignedHeaders=' + \
        signed_headers + ', ' + 'Signature=' + signature
    
    headers = {
        'X-Date': current_date,
        'Authorization': authorization_header,
        'X-Content-Sha256': payload_hash,
        'Content-Type': content_type
    }
    
    request_url = endpoint + '?' + canonical_querystring
    
    try:
        r = requests.post(request_url, headers=headers, data=req_body)
        return r
    except Exception as err:
        print(f'error occurred: {err}')
        raise


async def query_volcano_task_result(task_id: str):
    """
    查询火山引擎AI任务结果
    参数:
        task_id: 任务ID
    """
    try:
        # 获取访问密钥和私密密钥
        access_key = settings.VOLCANO_ACCESS_KEY
        secret_key = settings.VOLCANO_SECRET_KEY
        
        if not access_key or not secret_key:
            raise ValueError("VOLCANO_ACCESS_KEY或VOLCANO_SECRET_KEY未在配置文件中设置")
        
        # 构建请求参数
        query_params = {
            'Action': 'CVSync2AsyncGetResult',
            'Version': '2022-08-31',
        }
        
        body_params = {
            "req_key": "jimeng_t2i_v40",
            "task_id": task_id,
            "req_json": json.dumps({"return_url": True})
        }
        
        formatted_query = formatQuery(query_params)
        formatted_body = json.dumps(body_params)
        
        # 调用签名函数
        response = signV4Request(access_key, secret_key, service, formatted_query, formatted_body)
        
        # 打印响应状态码和内容
        print("Query Response Status Code:", response.status_code)
        print("Query Response Content:", response.text)
        
        # 解析响应结果
        result = response.json()
        
        # 提取任务结果数据
        if "data" in result:
            data = result["data"]
            print("Query Data section:", data)
            
            # 检查任务状态
            if "status" in data:
                status = data["status"]
                print("Task status:", status)
                
                # 如果任务已完成，检查是否有图片URL
                if status == "done" and "image_urls" in data and len(data["image_urls"]) > 0:
                    image_urls = data["image_urls"]
                    print("Image URLs:", image_urls)
                    # 返回第一张生成的图片URL
                    return image_urls[0]
                
                # 返回任务状态供前端判断
                return {"task_id": task_id, "status": status}
            
            # 如果没有status字段，但有image_urls字段
            if "image_urls" in data and len(data["image_urls"]) > 0:
                image_urls = data["image_urls"]
                print("Image URLs:", image_urls)
                # 返回第一张生成的图片URL
                return image_urls[0]
            
        raise ValueError("任务查询API返回结果格式不正确")
        
    except Exception as e:
        print("Error occurred in task query:", str(e))
        raise ValueError(f"查询火山引擎AI任务结果失败: {str(e)}")
