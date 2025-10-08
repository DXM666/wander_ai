import uvicorn
import os

if __name__ == "__main__":
    # 确保静态文件目录存在
    os.makedirs("static/uploads", exist_ok=True)
    os.makedirs("static/results", exist_ok=True)
    
    # 启动服务器
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
