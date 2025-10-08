from typing import Optional
from app.utils.volcano_api import call_volcano_image_api
from app.utils.volcano_task_query import query_volcano_task_result

async def generate_travel_photo(
    user_image_url: str,
    scene_image_url: str,
    location: str
):
    """
    生成旅游打卡照片服务
    参数:
        user_image_url: 用户照片URL地址
        scene_image_url: 场景照片URL地址
        location: 旅游地点
    """
    # 调用火山引擎API生成照片
    result = await call_volcano_image_api(user_image_url, scene_image_url, location)
    
    return result

async def query_travel_photo_result(task_id: str):
    """
    查询旅游打卡照片生成结果
    参数:
        task_id: 任务ID
    """
    # 调用火山引擎任务查询API
    result = await query_volcano_task_result(task_id)
    
    return result
