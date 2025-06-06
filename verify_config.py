#!/usr/bin/env python3
"""
配置验证脚本
检查火车沿途风景项目的所有配置是否正确
"""

import os
import requests
import json
from dotenv import load_dotenv

def check_env_file():
    """检查.env文件是否存在"""
    print("🔍 检查环境配置文件...")
    
    if os.path.exists('.env'):
        print("✅ .env 文件存在")
        return True
    else:
        print("❌ .env 文件不存在")
        print("   请运行: cp env.example .env")
        return False

def check_environment_variables():
    """检查环境变量"""
    print("\n🔍 检查环境变量...")
    
    load_dotenv()
    
    # 检查阿里百炼API配置
    alibaba_key = os.getenv("ALIBABA_DASHSCOPE_API_KEY")
    alibaba_app_id = os.getenv("ALIBABA_DASHSCOPE_APP_ID")
    
    # 检查高德地图API配置
    amap_key = os.getenv("AMAP_API_KEY")
    
    issues = []
    
    if not alibaba_key or alibaba_key == "your_dashscope_api_key_here":
        issues.append("阿里百炼API密钥未配置或为默认值")
    else:
        print("✅ 阿里百炼API密钥已配置")
    
    if not alibaba_app_id or alibaba_app_id == "your_app_id_here":
        issues.append("阿里百炼应用ID未配置或为默认值")
    else:
        print("✅ 阿里百炼应用ID已配置")
    
    if not amap_key or amap_key == "your_amap_api_key_here":
        issues.append("高德地图API密钥未配置或为默认值")
    else:
        print("✅ 高德地图API密钥已配置")
    
    if issues:
        print("\n⚠️ 发现配置问题:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    
    return True

def check_server_status():
    """检查服务器状态"""
    print("\n🔍 检查服务器状态...")
    
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 服务器运行正常")
            print(f"   - AI客户端: {data.get('ai_client', 'unknown')}")
            print(f"   - 图片服务: {data.get('image_service', 'unknown')}")
            print(f"   - 地图服务: {data.get('amap_service', 'unknown')}")
            return True
        else:
            print(f"❌ 服务器响应异常: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        print("   请先启动服务器: python main.py")
        return False
    except Exception as e:
        print(f"❌ 检查服务器时出错: {e}")
        return False

def check_map_config():
    """检查地图配置"""
    print("\n🔍 检查地图配置...")
    
    try:
        response = requests.get("http://localhost:8000/api/config/map", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('has_key'):
                print("✅ 高德地图配置正常")
                print(f"   - API密钥: {data.get('amap_api_key')[:10]}...")
                return True
            else:
                print("❌ 高德地图配置异常")
                print(f"   - 错误: {data.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ 获取地图配置失败: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 检查地图配置时出错: {e}")
        return False

def test_api_endpoints():
    """测试主要API端点"""
    print("\n🔍 测试API端点...")
    
    endpoints = [
        ("/api/health", "健康检查"),
        ("/api/config/map", "地图配置"),
    ]
    
    success_count = 0
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: 正常")
                success_count += 1
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {e}")
    
    return success_count == len(endpoints)

def generate_config_summary():
    """生成配置摘要"""
    print("\n📋 配置摘要:")
    
    load_dotenv()
    
    print("环境变量:")
    print(f"   - ALIBABA_DASHSCOPE_API_KEY: {'已配置' if os.getenv('ALIBABA_DASHSCOPE_API_KEY') else '未配置'}")
    print(f"   - ALIBABA_DASHSCOPE_APP_ID: {'已配置' if os.getenv('ALIBABA_DASHSCOPE_APP_ID') else '未配置'}")
    print(f"   - AMAP_API_KEY: {'已配置' if os.getenv('AMAP_API_KEY') else '未配置'}")
    
    print("\n配置文件:")
    print(f"   - .env文件: {'存在' if os.path.exists('.env') else '不存在'}")
    print(f"   - main.py: {'存在' if os.path.exists('main.py') else '不存在'}")
    print(f"   - static/index.html: {'存在' if os.path.exists('static/index.html') else '不存在'}")

def main():
    """主函数"""
    print("🔧 火车沿途风景项目配置验证")
    print("=" * 50)
    
    checks = [
        check_env_file(),
        check_environment_variables(),
        check_server_status(),
        check_map_config(),
        test_api_endpoints()
    ]
    
    passed = sum(checks)
    total = len(checks)
    
    print("\n" + "=" * 50)
    print(f"📊 验证结果: {passed}/{total} 项通过")
    
    if passed == total:
        print("🎉 所有配置检查通过！项目可以正常运行")
        print("\n🚀 启动说明:")
        print("   1. 确保服务器正在运行: python main.py")
        print("   2. 打开浏览器访问: http://localhost:8000")
        print("   3. 测试地图功能: 输入行程信息并选择车次")
    else:
        print("⚠️ 部分配置存在问题，请按照上述提示进行修复")
        
    generate_config_summary()

if __name__ == "__main__":
    main() 