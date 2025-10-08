from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.image_service import generate_travel_photo, query_travel_photo_result
from typing import Optional

router = APIRouter()

class TravelPhotoRequest(BaseModel):
    user_image_url: str
    scene_image_url: str
    location: str
    style: str = "natural"  # natural, artistic, vintage, modern, cinematic
    quality: str = "high"   # high, ultra, professional

@router.post("/generate-travel-photo")
async def generate_travel_photo_endpoint(request: TravelPhotoRequest):
    """
    生成旅游打卡照片API接口
    """
    try:
        # 调用图像生成服务
        result = await generate_travel_photo(
            request.user_image_url, 
            request.scene_image_url, 
            request.location,
            request.style,
            request.quality
        )
        
        return {
            "success": True,
            "result": result,
            "message": "照片生成任务已提交"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成照片失败: {str(e)}")

@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """
    查询任务状态API接口
    """
    try:
        # 调用任务查询服务
        result = await query_travel_photo_result(task_id)
        
        return {
            "success": True,
            "result": result,
            "message": "查询成功"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")
