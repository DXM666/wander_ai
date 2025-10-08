# 使用Python 3.12官方镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app/ ./app/
COPY main.py .
COPY .env .

# 创建静态文件目录
RUN mkdir -p static/uploads static/results

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["python", "main.py"]
