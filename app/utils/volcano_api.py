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


async def call_volcano_image_api(
    user_image_url: str,
    scene_image_url: str,
    location: str,
    style: str = "natural",
    quality: str = "high"
):
    """
    调用火山引擎AI绘画API生成旅游打卡照片
    参数:
        user_image_url: 用户照片URL地址
        scene_image_url: 场景照片URL地址
        location: 旅游地点
    """
    try:
        # 获取访问密钥和私密密钥
        access_key = settings.VOLCANO_ACCESS_KEY
        secret_key = settings.VOLCANO_SECRET_KEY
        
        if not access_key or not secret_key:
            raise ValueError("VOLCANO_ACCESS_KEY或VOLCANO_SECRET_KEY未在配置文件中设置")
        
        # 构建请求参数
        query_params = {
            'Action': 'CVSync2AsyncSubmitTask',
            'Version': '2022-08-31',
        }
        
        # 使用prompt构造工具生成优化的prompt
        from app.utils.prompt_builder import build_travel_photo_prompt
        enhanced_prompt = build_travel_photo_prompt(location, style, quality)
        
        body_params = {
            "req_key": "jimeng_t2i_v40",
            "prompt": enhanced_prompt,
            "image_urls": [user_image_url, scene_image_url],
            "req_json":{
                "return_url": True
            },
            "response_format": "url"
        }
        
        formatted_query = formatQuery(query_params)
        formatted_body = json.dumps(body_params)
        
        # 调用签名函数
        response = signV4Request(access_key, secret_key, service, formatted_query, formatted_body)
        
        # 打印响应状态码
        print("Response Status Code:", response.status_code)
        
        # 打印响应内容
        print("Response Content:", response.text)
        
        # 解析响应结果
        result = response.json()
        
        # 提取生成的图片数据
        if "data" in result:
            data = result["data"]
            print("Data section:", data)
            
            # 检查是否有task_id
            if "task_id" in data:
                task_id = data["task_id"]
                print("Task ID:", task_id)
                # 返回task_id，前端可以通过task_id查询任务状态
                return task_id
            
            # 如果没有task_id，但有其他可能的字段
            # 可以在这里添加更多的解析逻辑
            
        raise ValueError("API返回结果格式不正确")
    except Exception as e:
        print("Error occurred:", str(e))
        raise ValueError(f"调用火山引擎AI绘画API失败: {str(e)}")


def image_to_base64(image: Image.Image) -> str:
    """
    将PIL图像转换为base64编码字符串
    """
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str
