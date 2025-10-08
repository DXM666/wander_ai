"""
Prompt构造工具模块
用于生成优化的AI绘画提示词
"""

def build_travel_photo_prompt(location: str, style: str = "natural", quality: str = "high") -> str:
    """
    构造旅游打卡照片生成的prompt
    
    参数:
        location: 旅游地点
        style: 风格类型 (natural, artistic, vintage, modern)
        quality: 质量等级 (high, ultra, professional)
    """
    
    # 基础描述
    base_prompt = f"请将第一张人物照片中的人物自然地合成到第二张{location}风景照片中"
    
    # 风格描述映射
    style_descriptions = {
        "natural": "保持自然真实的效果，就像真实拍摄的旅游照片",
        "artistic": "增加艺术感和美感，色彩更加鲜艳生动",
        "vintage": "添加复古滤镜效果，温暖的色调和怀旧感",
        "modern": "现代时尚风格，清晰锐利，色彩饱和度高",
        "cinematic": "电影级别的光影效果，戏剧性的构图和色调"
    }
    
    # 质量描述映射
    quality_descriptions = {
        "high": "高质量",
        "ultra": "超高清4K质量，细节丰富",
        "professional": "专业摄影级别，完美的光线和构图"
    }
    
    # 技术要求
    technical_requirements = [
        "人物与背景光线、色调保持一致",
        "人物大小比例符合透视关系", 
        "边缘融合自然，无明显合成痕迹",
        "保持人物原有的姿态和表情",
        "整体画面和谐统一"
    ]
    
    # 构造完整prompt
    style_desc = style_descriptions.get(style, style_descriptions["natural"])
    quality_desc = quality_descriptions.get(quality, quality_descriptions["high"])
    
    enhanced_prompt = f"""
{base_prompt}，要求：
{chr(10).join([f"{i+1}. {req}" for i, req in enumerate(technical_requirements)])}
6. {style_desc}
生成{quality_desc}的旅游打卡照片效果。
    """.strip()
    
    return enhanced_prompt


def build_location_specific_prompt(location: str) -> dict:
    """
    根据地点生成特定的prompt增强信息
    
    参数:
        location: 旅游地点
        
    返回:
        包含特定描述和建议的字典
    """
    
    location_enhancements = {
        "巴黎埃菲尔铁塔": {
            "atmosphere": "浪漫的巴黎氛围，金色的夕阳光线",
            "composition": "埃菲尔铁塔作为背景，人物位于前景",
            "lighting": "温暖的黄昏光线，营造浪漫氛围"
        },
        "东京樱花": {
            "atmosphere": "春日樱花盛开的浪漫场景",
            "composition": "樱花树下的人物特写，粉色花瓣飘落",
            "lighting": "柔和的自然光，突出樱花的粉嫩色彩"
        },
        "纽约时代广场": {
            "atmosphere": "繁华都市的现代感和活力",
            "composition": "霓虹灯和广告牌作为背景，人物居中",
            "lighting": "城市夜景的霓虹灯光效果"
        },
        "马尔代夫海滩": {
            "atmosphere": "热带海岛的度假氛围",
            "composition": "蓝天白云和碧海为背景",
            "lighting": "明亮的阳光，清澈的海水反光"
        }
    }
    
    # 默认通用描述
    default_enhancement = {
        "atmosphere": "优美的旅游景点氛围",
        "composition": "景点作为背景，人物自然融入",
        "lighting": "适合的自然光线，突出景点特色"
    }
    
    return location_enhancements.get(location, default_enhancement)


def build_advanced_prompt(location: str, style: str = "natural", quality: str = "high", 
                         time_of_day: str = "auto", weather: str = "auto") -> str:
    """
    构造高级prompt，包含更多细节控制
    
    参数:
        location: 旅游地点
        style: 风格类型
        quality: 质量等级
        time_of_day: 时间 (morning, afternoon, evening, night, auto)
        weather: 天气 (sunny, cloudy, sunset, auto)
    """
    
    base_prompt = build_travel_photo_prompt(location, style, quality)
    location_info = build_location_specific_prompt(location)
    
    # 时间描述
    time_descriptions = {
        "morning": "清晨的柔和光线",
        "afternoon": "午后明亮的阳光", 
        "evening": "黄昏的温暖光线",
        "night": "夜晚的灯光效果"
    }
    
    # 天气描述
    weather_descriptions = {
        "sunny": "晴朗的天气，阳光充足",
        "cloudy": "多云的天空，柔和的散射光",
        "sunset": "日落时分，金色的光线"
    }
    
    # 添加额外描述
    additional_desc = []
    
    if time_of_day != "auto" and time_of_day in time_descriptions:
        additional_desc.append(time_descriptions[time_of_day])
        
    if weather != "auto" and weather in weather_descriptions:
        additional_desc.append(weather_descriptions[weather])
        
    additional_desc.append(location_info["atmosphere"])
    additional_desc.append(location_info["lighting"])
    
    if additional_desc:
        enhanced_prompt = f"{base_prompt}\n\n特殊要求：{', '.join(additional_desc)}"
    else:
        enhanced_prompt = base_prompt
        
    return enhanced_prompt
