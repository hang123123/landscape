#!/usr/bin/env python3
"""
前端后端集成测试脚本
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """测试API端点"""
    print("🧪 开始API测试...")
    
    # 1. 测试健康检查
    print("\n1️⃣ 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        health_data = response.json()
        print(f"✅ 健康检查通过: {health_data}")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False
    
    # 2. 测试车次搜索
    print("\n2️⃣ 测试车次搜索...")
    try:
        search_data = {
            "origin": "北京",
            "destination": "上海", 
            "departure_date": "2024-01-15"
        }
        response = requests.post(f"{BASE_URL}/api/search-trains", 
                               json=search_data)
        trains_data = response.json()
        print(f"✅ 车次搜索成功，找到 {len(trains_data['trains'])} 个车次")
        
        # 选择第一个车次进行下一步测试
        if trains_data['trains']:
            first_train = trains_data['trains'][0]
            print(f"   选择车次: {first_train['train_number']}")
            return first_train
        else:
            print("❌ 没有找到车次")
            return False
            
    except Exception as e:
        print(f"❌ 车次搜索失败: {e}")
        return False

def test_route_info(train_number):
    """测试路线信息"""
    print("\n3️⃣ 测试路线信息...")
    try:
        route_data = {
            "train_number": train_number,
            "origin": "北京",
            "destination": "上海"
        }
        response = requests.post(f"{BASE_URL}/api/get-route-info", 
                               json=route_data)
        route_info = response.json()
        
        print(f"✅ 路线信息获取成功")
        print(f"   路线: {route_info['route_info']['from_station']} → {route_info['route_info']['to_station']}")
        print(f"   沿途景点: {len(route_info['attractions'])} 个城市")
        print(f"   旅行贴士: {len(route_info.get('travel_tips', []))} 条")
        
        # 展示部分数据
        for i, attraction in enumerate(route_info['attractions'][:2]):
            print(f"   城市{i+1}: {attraction['city']} - {attraction['description'][:50]}...")
            
        return True
        
    except Exception as e:
        print(f"❌ 路线信息获取失败: {e}")
        return False

def test_frontend_page():
    """测试前端页面"""
    print("\n4️⃣ 测试前端页面...")
    try:
        response = requests.get(BASE_URL)
        if "火车沿途风景" in response.text:
            print("✅ 前端页面加载正常")
            return True
        else:
            print("❌ 前端页面内容异常")
            return False
    except Exception as e:
        print(f"❌ 前端页面测试失败: {e}")
        return False

def main():
    print("🚄 火车沿途风景 - 完整流程测试")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(2)
    
    # 测试前端页面
    if not test_frontend_page():
        return
    
    # 测试API端点
    train_number = test_api_endpoints()
    if not train_number:
        return
    
    # 测试路线信息
    if not test_route_info(train_number['train_number']):
        return
    
    print("\n🎉 所有测试通过！")
    print("\n📱 您可以访问以下地址：")
    print(f"   🏠 主页: {BASE_URL}")
    print(f"   📚 API文档: {BASE_URL}/docs")
    print(f"   ❤️ 健康检查: {BASE_URL}/api/health")
    
    print("\n💡 使用说明：")
    print("   1. 在主页填写始发站、终点站、出发日期")
    print("   2. 点击搜索，选择心仪的车次") 
    print("   3. 查看沿途的美丽风景和特色美食")

if __name__ == "__main__":
    main() 