from fastapi import UploadFile
import os
from PIL import Image
import io

async def process_images(user_photo: UploadFile, scene_photo: UploadFile):
    """
    处理上传的用户照片和场景照片
    """
    # 读取用户照片
    user_photo_content = await user_photo.read()
    user_image = Image.open(io.BytesIO(user_photo_content))
    
    # 读取场景照片
    scene_photo_content = await scene_photo.read()
    scene_image = Image.open(io.BytesIO(scene_photo_content))
    
    # 调整照片尺寸
    user_image = resize_image(user_image, (512, 512))
    scene_image = resize_image(scene_image, (512, 512))
    
    # 转换为RGB格式
    if user_image.mode != "RGB":
        user_image = user_image.convert("RGB")
    if scene_image.mode != "RGB":
        scene_image = scene_image.convert("RGB")
    
    return user_image, scene_image

def resize_image(image: Image.Image, size: tuple) -> Image.Image:
    """
    调整图像尺寸
    """
    return image.resize(size, Image.Resampling.LANCZOS)
