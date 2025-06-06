#!/usr/bin/env python3
"""
图片服务模块 - 提供稳定的图片API代理
"""

import requests
import hashlib
import os
import json
from pathlib import Path
from typing import Optional, List, Dict
import random
import time

class ImageService:
    """图片服务类"""
    
    def __init__(self):
        self.cache_dir = Path("image_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        # 预定义的高质量图片池
        self.attraction_images = {
            '北京': [
                'https://images.unsplash.com/photo-1508804185872-d7badad00f7d', # 故宫
                'https://images.unsplash.com/photo-1591522811280-a8759970b03f', # 长城
                'https://images.unsplash.com/photo-1570894842629-3c7c1db9f825', # 天坛
                'https://images.unsplash.com/photo-1545893835-abaa50cbe628'  # 北京夜景
            ],
            '上海': [
                'https://images.unsplash.com/photo-1474181487882-5abf3f0ba6c2', # 外滩
                'https://images.unsplash.com/photo-1519368358672-25b03afee3bf', # 陆家嘴
                'https://images.unsplash.com/photo-1591154669695-5f2a8d20c089', # 东方明珠
                'https://images.unsplash.com/photo-1567088367166-d894e8c7a07e'  # 上海夜景
            ],
            '天津': [
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4', # 建筑
                'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df', # 欧式建筑
                'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0', # 历史建筑
                'https://images.unsplash.com/photo-1520637836862-4d197d17c55a'  # 城市景观
            ],
            '济南': [
                'https://images.unsplash.com/photo-1518837695005-2083093ee35b', # 泉水
                'https://images.unsplash.com/photo-1441974231531-c6227db76b6e', # 湖泊
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4', # 园林
                'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0'  # 古建筑
            ]
        }
        
        self.food_images = {
            '北京': [
                'https://images.unsplash.com/photo-1544584244-6334889fffe7', # 烤鸭
                'https://images.unsplash.com/photo-1569718212165-3a8278d5f624', # 中式面条
                'https://images.unsplash.com/photo-1583337130417-3346a1be7dee', # 中式早餐
                'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445'  # 中式糕点
            ],
            '上海': [
                'https://images.unsplash.com/photo-1496116218417-1a781b1c416c', # 小笼包
                'https://images.unsplash.com/photo-1585759065152-348fea993c5c', # 生煎包
                'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b', # 中式菜肴
                'https://images.unsplash.com/photo-1570197788417-0e82375c9371'  # 海鲜
            ],
            '天津': [
                'https://images.unsplash.com/photo-1563379091339-03246efb6822', # 包子
                'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b', # 煎饼
                'https://images.unsplash.com/photo-1546833999-b9f581a1996d', # 传统糕点
                'https://images.unsplash.com/photo-1578985545062-69928b1d9587'  # 麻花
            ],
            '济南': [
                'https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43', # 把子肉
                'https://images.unsplash.com/photo-1516684732162-798a0062be99', # 粥类
                'https://images.unsplash.com/photo-1551782450-17144efb9c50', # 烘培
                'https://images.unsplash.com/photo-1565958011703-44f9829ba187'  # 鱼类菜肴
            ]
        }
        
        # 通用备选图片
        self.fallback_attractions = [
            'https://images.unsplash.com/photo-1439066615861-d1af74d74000',
            'https://images.unsplash.com/photo-1469474968028-56623f02e42e',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4',
            'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0'
        ]
        
        self.fallback_foods = [
            'https://images.unsplash.com/photo-1504674900247-0877df9cc836',
            'https://images.unsplash.com/photo-1555939594-58d7cb561ad1',
            'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b',
            'https://images.unsplash.com/photo-1546833999-b9f581a1996d'
        ]
    
    def get_attraction_image(self, spot: str, city: str, index: int = 0) -> str:
        """获取景点图片URL"""
        # 首先尝试城市特定图片
        city_images = self.attraction_images.get(city, [])
        if city_images:
            return city_images[index % len(city_images)] + '?w=400&h=300&fit=crop&crop=center'
        
        # 使用通用景点图片
        return self.fallback_attractions[index % len(self.fallback_attractions)] + '?w=400&h=300&fit=crop&crop=center'
    
    def get_food_image(self, food: str, city: str, index: int = 0) -> str:
        """获取美食图片URL"""
        # 首先尝试城市特定图片
        city_foods = self.food_images.get(city, [])
        if city_foods:
            return city_foods[index % len(city_foods)] + '?w=400&h=300&fit=crop&crop=center'
        
        # 使用通用美食图片
        return self.fallback_foods[index % len(self.fallback_foods)] + '?w=400&h=300&fit=crop&crop=center'
    
    def get_image_urls_batch(self, attractions: List[Dict]) -> Dict:
        """批量获取图片URL"""
        result = {
            'attractions': [],
            'status': 'success'
        }
        
        for attraction in attractions:
            city = attraction.get('city', '')
            
            # 处理景点图片
            scenic_spots_with_images = []
            for i, spot in enumerate(attraction.get('scenic_spots', [])):
                image_url = self.get_attraction_image(spot, city, i)
                scenic_spots_with_images.append({
                    'name': spot,
                    'image': image_url
                })
            
            # 处理美食图片
            local_food_with_images = []
            for i, food in enumerate(attraction.get('local_food', [])):
                image_url = self.get_food_image(food, city, i)
                local_food_with_images.append({
                    'name': food,
                    'image': image_url
                })
            
            result['attractions'].append({
                'city': city,
                'description': attraction.get('description', ''),
                'scenic_spots': scenic_spots_with_images,
                'local_food': local_food_with_images
            })
        
        return result
    
    def validate_image_url(self, url: str) -> bool:
        """验证图片URL是否可访问"""
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_random_images(self, category: str, count: int = 4) -> List[str]:
        """获取随机图片"""
        if category == 'attraction':
            all_images = []
            for city_images in self.attraction_images.values():
                all_images.extend(city_images)
            all_images.extend(self.fallback_attractions)
        else:  # food
            all_images = []
            for city_foods in self.food_images.values():
                all_images.extend(city_foods)
            all_images.extend(self.fallback_foods)
        
        selected = random.sample(all_images, min(count, len(all_images)))
        return [img + '?w=400&h=300&fit=crop&crop=center' for img in selected]

# 全局图片服务实例
image_service = ImageService()

if __name__ == "__main__":
    # 测试图片服务
    service = ImageService()
    
    # 测试数据
    test_attractions = [
        {
            'city': '北京',
            'description': '中国首都，历史文化名城',
            'scenic_spots': ['故宫', '天安门', '长城'],
            'local_food': ['烤鸭', '炸酱面', '豆汁']
        },
        {
            'city': '上海',
            'description': '国际大都市',
            'scenic_spots': ['外滩', '东方明珠', '豫园'],
            'local_food': ['小笼包', '生煎包', '白切鸡']
        }
    ]
    
    result = service.get_image_urls_batch(test_attractions)
    print(json.dumps(result, ensure_ascii=False, indent=2)) 