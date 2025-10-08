from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="WanderAI Backend", description="AI旅游打卡照片生成服务后端")

# 注册API路由
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to WanderAI Backend API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
