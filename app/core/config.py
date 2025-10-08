import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class Settings:
    # 火山引擎API配置
    VOLCANO_ACCESS_KEY: str = os.getenv("VOLCANO_ACCESS_KEY")
    VOLCANO_SECRET_KEY: str = os.getenv("VOLCANO_SECRET_KEY")
    VOLCANO_REGION: str = os.getenv("VOLCANO_REGION", "cn-north-1")
    
    # 应用配置
    APP_NAME: str = "WanderAI Backend"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # 静态文件配置
    STATIC_FOLDER: str = os.getenv("STATIC_FOLDER", "static")
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "static/uploads")
    RESULT_FOLDER: str = os.getenv("RESULT_FOLDER", "static/results")

settings = Settings()
