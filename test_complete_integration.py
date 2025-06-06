#!/usr/bin/env python3
"""
完整功能集成测试
测试火车沿途风景项目的所有核心功能
"""

import requests
import json
import asyncio
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 健康检查通过")
            print(f"   - AI客户端: {data.get('ai_client')}")
            print(f"   - 图片服务: {data.get('image_service')}")
            print(f"   - 地图服务: {data.get('amap_service')}")
            return True
        else:
            print(f"❌ 健康检查失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_map_config():
    """测试地图配置"""
    print("\n🔍 测试地图配置...")
    try:
        response = requests.get(f"{BASE_URL}/api/config/map")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('has_key'):
                print("✅ 地图配置正常")
                print(f"   - API密钥: {data.get('amap_api_key')[:10]}...")
                return True
            else:
                print("❌ 地图配置异常")
                return False
        else:
            print(f"❌ 地图配置失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 地图配置失败: {e}")
        return False

def test_train_search():
    """测试车次搜索"""
    print("\n🔍 测试车次搜索...")
    try:
        # 计算明天的日期
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        data = {
            "origin": "北京",
            "destination": "上海",
            "departure_date": tomorrow
        }
        
        response = requests.post(
            f"{BASE_URL}/api/search-trains",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 车次搜索成功")
            print(f"   - 找到车次数量: {result.get('count', 0)}")
            if result.get('trains'):
                sample_train = result['trains'][0]
                print(f"   - 示例车次: {sample_train.get('train_number', 'N/A')}")
                return True, result['trains'][0] if result.get('trains') else None
            return True, None
        else:
            print(f"❌ 车次搜索失败: HTTP {response.status_code}")
            return False, None
    except Exception as e:
        print(f"❌ 车次搜索失败: {e}")
        return False, None

def test_route_info(train_data=None):
    """测试路线信息"""
    print("\n🔍 测试路线信息...")
    try:
        data = {
            "train_number": train_data.get('train_number', 'G101') if train_data else "G101",
            "origin": "北京南",
            "destination": "上海虹桥"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/get-route-info",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 路线信息获取成功")
            if result.get('attractions'):
                print(f"   - 沿途城市数量: {len(result['attractions'])}")
                for i, city in enumerate(result['attractions'][:3]):  # 显示前3个城市
                    print(f"   - 城市{i+1}: {city.get('city', 'N/A')}")
            return True, result
        else:
            print(f"❌ 路线信息获取失败: HTTP {response.status_code}")
            return False, None
    except Exception as e:
        print(f"❌ 路线信息获取失败: {e}")
        return False, None

def test_route_stations(train_data=None):
    """测试站点信息"""
    print("\n🔍 测试站点信息...")
    try:
        data = {
            "train_number": train_data.get('train_number', 'G101') if train_data else "G101",
            "origin": "北京南",
            "destination": "上海虹桥"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/get-route-stations",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 站点信息获取成功")
                stations = result.get('data', {}).get('stations', [])
                print(f"   - 途径站点数量: {len(stations)}")
                
                for i, station in enumerate(stations[:3]):  # 显示前3个站点
                    print(f"   - 站点{i+1}: {station.get('name', 'N/A')} ({station.get('city', 'N/A')})")
                
                # 验证坐标数据
                coords_valid = all(
                    isinstance(s.get('longitude'), (int, float)) and 
                    isinstance(s.get('latitude'), (int, float))
                    for s in stations
                )
                print(f"   - 坐标数据: {'✅ 有效' if coords_valid else '❌ 无效'}")
                
                return True, result
            else:
                print(f"❌ 站点信息获取失败: {result.get('message', '未知错误')}")
                return False, None
        else:
            print(f"❌ 站点信息获取失败: HTTP {response.status_code}")
            return False, None
    except Exception as e:
        print(f"❌ 站点信息获取失败: {e}")
        return False, None

def test_frontend_accessibility():
    """测试前端可访问性"""
    print("\n🔍 测试前端页面...")
    try:
        response = requests.get(BASE_URL)
        
        if response.status_code == 200:
            print("✅ 前端页面可访问")
            # 检查是否包含关键元素
            content = response.text
            key_elements = [
                "火车沿途风景",
                "搜索列车",
                "route-map",
                "amap.com"
            ]
            
            found_elements = [elem for elem in key_elements if elem in content]
            print(f"   - 关键元素: {len(found_elements)}/{len(key_elements)} 找到")
            
            return len(found_elements) >= 3  # 至少找到3个关键元素
        else:
            print(f"❌ 前端页面不可访问: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端页面访问失败: {e}")
        return False

def generate_test_report(results):
    """生成测试报告"""
    print("\n" + "="*60)
    print("📋 完整功能测试报告")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"📊 总体结果: {passed}/{total} 项通过 ({success_rate:.1f}%)")
    print("\n详细结果:")
    
    test_names = {
        'health': '健康检查',
        'map_config': '地图配置',
        'train_search': '车次搜索',
        'route_info': '路线信息',
        'route_stations': '站点信息',
        'frontend': '前端页面'
    }
    
    for key, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"   - {test_names.get(key, key)}: {status}")
    
    print("\n" + "="*60)
    
    if success_rate == 100:
        print("🎉 所有测试通过！项目功能完整")
        print("\n🚀 使用说明:")
        print("   1. 服务器已在 http://localhost:8000 运行")
        print("   2. 打开浏览器访问主页")
        print("   3. 输入出发地、目的地和日期")
        print("   4. 选择车次后即可查看地图和景点信息")
    elif success_rate >= 80:
        print("⚠️ 大部分功能正常，少量问题需要修复")
    else:
        print("❌ 存在较多问题，需要全面检查")
    
    return success_rate

def main():
    """主测试函数"""
    print("🧪 开始完整功能集成测试")
    print("="*60)
    
    results = {}
    train_data = None
    
    # 1. 健康检查
    results['health'] = test_health_check()
    
    # 2. 地图配置
    results['map_config'] = test_map_config()
    
    # 3. 车次搜索
    search_success, train_data = test_train_search()
    results['train_search'] = search_success
    
    # 4. 路线信息
    route_success, route_data = test_route_info(train_data)
    results['route_info'] = route_success
    
    # 5. 站点信息
    stations_success, stations_data = test_route_stations(train_data)
    results['route_stations'] = stations_success
    
    # 6. 前端页面
    results['frontend'] = test_frontend_accessibility()
    
    # 生成报告
    success_rate = generate_test_report(results)
    
    return success_rate >= 80

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 