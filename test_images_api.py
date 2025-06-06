#!/usr/bin/env python3
"""
图片API测试脚本
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_image_apis():
    """测试图片相关的API端点"""
    print("🖼️ 图片API测试开始...")
    
    # 1. 测试健康检查（包含图片服务状态）
    print("\n1️⃣ 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        health_data = response.json()
        print(f"✅ 健康检查: {health_data}")
        
        if health_data.get('image_service') != 'connected':
            print("⚠️ 图片服务未正确连接")
            
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False
    
    # 2. 测试特定城市景点图片
    print("\n2️⃣ 测试城市景点图片API...")
    cities = ['北京', '上海', '天津', '济南']
    
    for city in cities:
        try:
            response = requests.get(f"{BASE_URL}/api/images/attractions/{city}?count=3")
            data = response.json()
            
            if data['status'] == 'success':
                print(f"✅ {city}景点图片: {len(data['images'])} 张")
                for img in data['images'][:2]:  # 显示前2张
                    print(f"   - {img['url']}")
            else:
                print(f"❌ {city}景点图片获取失败")
                
        except Exception as e:
            print(f"❌ {city}景点图片API错误: {e}")
    
    # 3. 测试特定城市美食图片
    print("\n3️⃣ 测试城市美食图片API...")
    
    for city in cities:
        try:
            response = requests.get(f"{BASE_URL}/api/images/foods/{city}?count=3")
            data = response.json()
            
            if data['status'] == 'success':
                print(f"✅ {city}美食图片: {len(data['images'])} 张")
                for img in data['images'][:2]:  # 显示前2张
                    print(f"   - {img['url']}")
            else:
                print(f"❌ {city}美食图片获取失败")
                
        except Exception as e:
            print(f"❌ {city}美食图片API错误: {e}")
    
    # 4. 测试随机图片API
    print("\n4️⃣ 测试随机图片API...")
    
    for category in ['attraction', 'food']:
        try:
            response = requests.get(f"{BASE_URL}/api/images/random?category={category}&count=4")
            data = response.json()
            
            if data['status'] == 'success':
                print(f"✅ 随机{category}图片: {len(data['images'])} 张")
                for img in data['images'][:2]:
                    print(f"   - {img['url']}")
            else:
                print(f"❌ 随机{category}图片获取失败")
                
        except Exception as e:
            print(f"❌ 随机{category}图片API错误: {e}")
    
    # 5. 测试批量图片API
    print("\n5️⃣ 测试批量图片API...")
    
    test_attractions = [
        {
            'city': '北京',
            'description': '中国首都',
            'scenic_spots': ['故宫', '天安门'],
            'local_food': ['烤鸭', '炸酱面']
        },
        {
            'city': '上海',
            'description': '国际大都市',
            'scenic_spots': ['外滩', '东方明珠'],
            'local_food': ['小笼包', '生煎包']
        }
    ]
    
    try:
        response = requests.post(f"{BASE_URL}/api/images/batch", json=test_attractions)
        data = response.json()
        
        if data['status'] == 'success':
            print(f"✅ 批量图片处理成功: {len(data['attractions'])} 个城市")
            
            for attraction in data['attractions']:
                print(f"   📍 {attraction['city']}:")
                print(f"      景点: {len(attraction['scenic_spots'])} 个")
                print(f"      美食: {len(attraction['local_food'])} 个")
                
                # 显示第一个景点和美食的图片URL
                if attraction['scenic_spots']:
                    spot = attraction['scenic_spots'][0]
                    print(f"      示例景点: {spot['name']} - {spot['image'][:50]}...")
                
                if attraction['local_food']:
                    food = attraction['local_food'][0]
                    print(f"      示例美食: {food['name']} - {food['image'][:50]}...")
        else:
            print(f"❌ 批量图片处理失败")
            
    except Exception as e:
        print(f"❌ 批量图片API错误: {e}")
    
    # 6. 测试完整路线信息API（包含图片）
    print("\n6️⃣ 测试完整路线信息API...")
    
    try:
        route_data = {
            "train_number": "G101",
            "origin": "北京",
            "destination": "上海"
        }
        response = requests.post(f"{BASE_URL}/api/get-route-info", json=route_data)
        data = response.json()
        
        if 'attractions' in data:
            print(f"✅ 路线信息API成功: {len(data['attractions'])} 个城市")
            
            for attraction in data['attractions']:
                print(f"   📍 {attraction['city']}:")
                
                # 检查景点是否有图片
                has_spot_images = all('image' in spot for spot in attraction['scenic_spots'] if isinstance(spot, dict))
                has_food_images = all('image' in food for food in attraction['local_food'] if isinstance(food, dict))
                
                spot_status = "✅ 有图片" if has_spot_images else "❌ 缺少图片"
                food_status = "✅ 有图片" if has_food_images else "❌ 缺少图片"
                
                print(f"      景点: {len(attraction['scenic_spots'])} 个 {spot_status}")
                print(f"      美食: {len(attraction['local_food'])} 个 {food_status}")
        else:
            print(f"❌ 路线信息API数据格式错误")
            
    except Exception as e:
        print(f"❌ 路线信息API错误: {e}")
    
    print("\n🎉 图片API测试完成！")

def test_image_urls_accessibility():
    """测试图片URL的可访问性"""
    print("\n🔗 测试图片URL可访问性...")
    
    # 测试一些图片URL
    test_urls = [
        "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=400&h=300&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1544584244-6334889fffe7?w=400&h=300&fit=crop&crop=center",
        "https://picsum.photos/400/300?random=test"
    ]
    
    accessible_count = 0
    
    for url in test_urls:
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ 可访问: {url[:50]}...")
                accessible_count += 1
            else:
                print(f"⚠️ 状态码 {response.status_code}: {url[:50]}...")
        except Exception as e:
            print(f"❌ 无法访问: {url[:50]}... ({e})")
    
    print(f"\n📊 可访问性统计: {accessible_count}/{len(test_urls)} 个URL可访问")

def main():
    print("🖼️ 火车沿途风景 - 图片系统完整测试")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(2)
    
    # 测试图片API
    test_image_apis()
    
    # 测试图片URL可访问性
    test_image_urls_accessibility()
    
    print("\n💡 提示：")
    print("   🌐 访问 http://localhost:8000/test-images 查看图片测试页面")
    print("   🏠 访问 http://localhost:8000 体验完整应用")

if __name__ == "__main__":
    main() 