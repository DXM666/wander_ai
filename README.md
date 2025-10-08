# WanderAI - AI旅游打卡照片生成服务

## 项目简介

WanderAI 是一个基于AI技术的旅游打卡照片生成服务，用户可以通过上传自拍照片和选择旅游地点，利用火山引擎AI绘画API生成逼真的旅游打卡照片，实现"足不出户环游世界"的沉浸式体验。

## 核心功能

- 🌍 **智能照片合成**: 将用户照片自然合成到世界各地的风景照片中
- 🎨 **多种风格选择**: 支持自然、艺术、复古、现代、电影等多种风格
- 📸 **高质量输出**: 提供高清、超高清、专业级等多种质量选项
- 🚀 **异步处理**: 采用任务队列模式，支持大量并发请求
- 📍 **地点优化**: 针对热门旅游地点提供专门的prompt优化

## 技术架构

### 后端技术栈
- **Python 3.12+**: 主要开发语言
- **FastAPI**: 现代化的Web框架
- **Uvicorn**: ASGI服务器
- **火山引擎AI绘画API**: 核心图像生成服务
- **Pydantic**: 数据验证和序列化

### 项目结构
```
wander_ai/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # API路由定义
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # 配置管理
│   ├── services/
│   │   ├── __init__.py
│   │   └── image_service.py   # 图像生成服务
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── volcano_api.py     # 火山引擎API调用
│   │   ├── volcano_task_query.py  # 任务查询
│   │   ├── prompt_builder.py  # Prompt构造工具
│   │   └── image_utils.py     # 图像处理工具
│   └── __init__.py
├── .env                       # 环境变量配置
├── .gitignore
├── main.py                    # 应用入口
├── requirements.txt           # 依赖包列表
└── README.md                  # 项目文档
```

## 快速开始

### 1. 环境准备

确保已安装Python 3.12+和uv包管理器：

```bash
# 安装uv (如果尚未安装)
pip install uv
```

### 2. 克隆项目

```bash
git clone <repository-url>
cd wander_ai
```

### 3. 创建虚拟环境

```bash
uv venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 4. 安装依赖

```bash
uv pip install -r requirements.txt
```

### 5. 配置环境变量

复制 `.env` 文件并填入您的火山引擎API密钥：

```bash
# 火山引擎API配置
VOLCANO_ACCESS_KEY=your_access_key_here
VOLCANO_SECRET_KEY=your_secret_key_here
VOLCANO_REGION=cn-north-1
```

### 6. 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

## API接口文档

### 1. 生成旅游打卡照片

**接口**: `POST /api/generate-travel-photo`

**请求体**:
```json
{
    "user_image_url": "https://example.com/user_photo.jpg",
    "scene_image_url": "https://example.com/scene_photo.jpg",
    "location": "巴黎埃菲尔铁塔",
    "style": "natural",
    "quality": "high"
}
```

**参数说明**:
- `user_image_url`: 用户照片URL地址
- `scene_image_url`: 场景照片URL地址  
- `location`: 旅游地点名称
- `style`: 风格类型 (可选)
  - `natural`: 自然真实效果 (默认)
  - `artistic`: 艺术感和美感
  - `vintage`: 复古滤镜效果
  - `modern`: 现代时尚风格
  - `cinematic`: 电影级光影效果
- `quality`: 质量等级 (可选)
  - `high`: 高质量 (默认)
  - `ultra`: 超高清4K质量
  - `professional`: 专业摄影级别

**响应示例**:
```json
{
    "success": true,
    "result": "7392616336519610409",
    "message": "照片生成任务已提交"
}
```

### 2. 查询任务状态

**接口**: `GET /api/task-status/{task_id}`

**响应示例**:
```json
{
    "success": true,
    "result": "https://example.com/generated_photo.jpg",
    "message": "查询成功"
}
```

## 火山引擎配置

### 1. 注册账号
访问 [火山引擎控制台](https://console.volcengine.com/) 注册账号

### 2. 开通服务
- 开通方舟（Ark）服务
- 开通 `doubao-seedream-4-0-250828` 模型

### 3. 获取API密钥
在控制台获取 Access Key 和 Secret Key

### 4. 配置限制
- 提示词建议 ≤300 汉字或 600 英文单词
- 参考图最多 10 张，每张 ≤10MB
- 组图生成：参考图 + 生成图总数 ≤15 张
- URL 格式的图片链接 24 小时后失效

## 开发指南

### 添加新的风格

1. 在 `app/utils/prompt_builder.py` 中的 `style_descriptions` 字典添加新风格
2. 更新API文档中的风格说明

### 添加新的地点优化

1. 在 `prompt_builder.py` 中的 `location_enhancements` 字典添加地点信息
2. 包含氛围、构图、光线等描述

### 自定义Prompt

可以通过修改 `build_travel_photo_prompt` 函数来自定义prompt生成逻辑。

## 部署说明

### Docker部署 (推荐)

```bash
# 构建镜像
docker build -t wander-ai .

# 运行容器
docker run -d -p 8000:8000 --env-file .env wander-ai
```

### 生产环境部署

```bash
# 使用Gunicorn部署
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 常见问题

### Q: 生成的照片质量不理想怎么办？
A: 可以尝试调整以下参数：
- 使用更高的质量等级 (`ultra` 或 `professional`)
- 选择合适的风格类型
- 确保输入图片质量良好

### Q: 任务一直处于处理状态？
A: 图像生成需要一定时间，建议：
- 等待1-3分钟后再查询
- 检查火山引擎API配额是否充足
- 确认网络连接正常

### Q: API调用失败？
A: 请检查：
- 火山引擎API密钥是否正确
- 图片URL是否可访问
- 图片大小是否超过限制

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件至：[your-email@example.com]

## 更新日志

### v1.0.0 (2025-10-08)
- ✨ 初始版本发布
- 🎨 支持多种风格和质量选项
- 🚀 异步任务处理
- 📍 地点特定优化
- 📚 完整的API文档

---

**WanderAI** - 让每个人都能拥有环游世界的美好回忆 🌍✨
