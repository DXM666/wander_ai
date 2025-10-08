# WanderAI API 接口文档

## 基础信息

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`
- **API版本**: v1.0

## 接口列表

### 1. 健康检查

**接口**: `GET /`

**描述**: 检查服务是否正常运行

**响应示例**:
```json
{
    "message": "Welcome to WanderAI Backend API"
}
```

---

### 2. 生成旅游打卡照片

**接口**: `POST /api/generate-travel-photo`

**描述**: 提交照片生成任务，将用户照片合成到指定旅游地点

**请求头**:
```
Content-Type: application/json
```

**请求参数**:
```json
{
    "user_image_url": "string",     // 必填：用户照片URL
    "scene_image_url": "string",    // 必填：场景照片URL  
    "location": "string",           // 必填：旅游地点名称
    "style": "string",              // 可选：风格类型，默认"natural"
    "quality": "string"             // 可选：质量等级，默认"high"
}
```

**参数详细说明**:

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| user_image_url | string | 是 | - | 用户照片的URL地址，支持http/https |
| scene_image_url | string | 是 | - | 场景照片的URL地址，支持http/https |
| location | string | 是 | - | 旅游地点名称，如"巴黎埃菲尔铁塔" |
| style | string | 否 | "natural" | 风格类型，见下表 |
| quality | string | 否 | "high" | 质量等级，见下表 |

**风格类型 (style)**:
| 值 | 说明 |
|----|------|
| natural | 自然真实效果，像真实拍摄的旅游照片 |
| artistic | 艺术感和美感，色彩更加鲜艳生动 |
| vintage | 复古滤镜效果，温暖的色调和怀旧感 |
| modern | 现代时尚风格，清晰锐利，色彩饱和度高 |
| cinematic | 电影级别的光影效果，戏剧性的构图和色调 |

**质量等级 (quality)**:
| 值 | 说明 |
|----|------|
| high | 高质量输出 |
| ultra | 超高清4K质量，细节丰富 |
| professional | 专业摄影级别，完美的光线和构图 |

**请求示例**:
```json
{
    "user_image_url": "https://example.com/user_selfie.jpg",
    "scene_image_url": "https://example.com/eiffel_tower.jpg",
    "location": "巴黎埃菲尔铁塔",
    "style": "natural",
    "quality": "high"
}
```

**成功响应**:
```json
{
    "success": true,
    "result": "7392616336519610409",
    "message": "照片生成任务已提交"
}
```

**错误响应**:
```json
{
    "detail": "生成照片失败: 具体错误信息"
}
```

**状态码**:
- `200`: 请求成功
- `422`: 参数验证失败
- `500`: 服务器内部错误

---

### 3. 查询任务状态

**接口**: `GET /api/task-status/{task_id}`

**描述**: 查询照片生成任务的状态和结果

**路径参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| task_id | string | 是 | 任务ID，由生成接口返回 |

**请求示例**:
```
GET /api/task-status/7392616336519610409
```

**成功响应 - 任务完成**:
```json
{
    "success": true,
    "result": "https://example.com/generated_photo.jpg",
    "message": "查询成功"
}
```

**成功响应 - 任务进行中**:
```json
{
    "success": true,
    "result": {
        "task_id": "7392616336519610409",
        "status": "processing"
    },
    "message": "查询成功"
}
```

**错误响应**:
```json
{
    "detail": "查询失败: 任务不存在或已过期"
}
```

**状态码**:
- `200`: 请求成功
- `404`: 任务不存在
- `500`: 服务器内部错误

## 使用流程

1. **提交生成任务**: 调用 `/api/generate-travel-photo` 接口，获取任务ID
2. **轮询查询状态**: 使用任务ID调用 `/api/task-status/{task_id}` 接口
3. **获取结果**: 当任务完成时，接口返回生成的照片URL

## 错误码说明

| HTTP状态码 | 说明 |
|------------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 422 | 参数验证失败 |
| 500 | 服务器内部错误 |

## 限制说明

### 图片要求
- 支持格式：JPG, JPEG, PNG
- 单张图片大小：≤10MB
- 图片URL必须可公开访问

### 提示词限制
- 地点名称建议≤50个字符
- 系统会自动优化生成详细的提示词

### 任务限制
- 任务结果保留24小时
- 建议及时下载生成的照片
- 单次最多处理2张输入图片

## 示例代码

### JavaScript (Fetch API)
```javascript
// 生成照片
async function generatePhoto() {
    const response = await fetch('/api/generate-travel-photo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_image_url: 'https://example.com/user.jpg',
            scene_image_url: 'https://example.com/scene.jpg',
            location: '巴黎埃菲尔铁塔',
            style: 'natural',
            quality: 'high'
        })
    });
    
    const result = await response.json();
    return result.result; // 返回task_id
}

// 查询状态
async function checkStatus(taskId) {
    const response = await fetch(`/api/task-status/${taskId}`);
    const result = await response.json();
    return result;
}
```

### Python (requests)
```python
import requests
import time

# 生成照片
def generate_photo():
    url = 'http://localhost:8000/api/generate-travel-photo'
    data = {
        'user_image_url': 'https://example.com/user.jpg',
        'scene_image_url': 'https://example.com/scene.jpg',
        'location': '巴黎埃菲尔铁塔',
        'style': 'natural',
        'quality': 'high'
    }
    
    response = requests.post(url, json=data)
    return response.json()['result']

# 查询状态
def check_status(task_id):
    url = f'http://localhost:8000/api/task-status/{task_id}'
    response = requests.get(url)
    return response.json()

# 完整流程
def generate_and_wait():
    # 提交任务
    task_id = generate_photo()
    print(f"任务已提交，ID: {task_id}")
    
    # 轮询查询
    while True:
        result = check_status(task_id)
        if isinstance(result['result'], str) and result['result'].startswith('http'):
            print(f"生成完成: {result['result']}")
            break
        else:
            print("任务进行中...")
            time.sleep(5)
```

### cURL
```bash
# 生成照片
curl -X POST "http://localhost:8000/api/generate-travel-photo" \
     -H "Content-Type: application/json" \
     -d '{
       "user_image_url": "https://example.com/user.jpg",
       "scene_image_url": "https://example.com/scene.jpg", 
       "location": "巴黎埃菲尔铁塔",
       "style": "natural",
       "quality": "high"
     }'

# 查询状态
curl -X GET "http://localhost:8000/api/task-status/7392616336519610409"
```

## 常见问题

### Q: 为什么使用异步任务模式？
A: AI图像生成需要较长时间（通常1-3分钟），异步模式可以避免HTTP请求超时，提供更好的用户体验。

### Q: 如何处理任务失败？
A: 查询接口会返回具体的错误信息，建议根据错误类型进行重试或提示用户。

### Q: 生成的照片URL什么时候失效？
A: 根据火山引擎API限制，生成的图片URL在24小时后失效，建议及时下载保存。

### Q: 支持批量生成吗？
A: 当前版本不支持批量生成，需要逐个提交任务。后续版本会考虑添加批量处理功能。
