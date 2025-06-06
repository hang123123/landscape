#!/usr/bin/env python3
"""
调试脚本：测试前端请求格式以找出422错误的原因
"""

import json
import requests
import asyncio

# 测试数据
test_data = {
    "train_number": "G101",
    "origin": "北京",
    "destination": "上海"
}

def test_api_endpoint():
    """测试API端点"""
    print("=== 测试 get-route-info 端点 ===")
    
    url = "http://localhost:8000/api/get-route-info"
    headers = {"Content-Type": "application/json"}
    
    print(f"请求URL: {url}")
    print(f"请求头: {headers}")
    print(f"请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=test_data)
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ 请求成功!")
            result = response.json()
            print(f"响应数据类型: {type(result)}")
            if 'success' in result:
                print(f"成功状态: {result['success']}")
        elif response.status_code == 422:
            print("❌ 422 验证错误!")
            error_detail = response.json()
            print(f"错误详情: {json.dumps(error_detail, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 其他错误: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败 - 确保服务器正在运行")
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_stations_endpoint():
    """测试站点信息端点"""
    print("\n=== 测试 get-route-stations 端点 ===")
    
    url = "http://localhost:8000/api/get-route-stations"
    headers = {"Content-Type": "application/json"}
    
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=test_data)
        
        print(f"\n响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 请求成功!")
        elif response.status_code == 422:
            print("❌ 422 验证错误!")
            error_detail = response.json()
            print(f"错误详情: {json.dumps(error_detail, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 其他错误: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败 - 确保服务器正在运行")
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_malformed_requests():
    """测试各种可能导致422的请求格式"""
    print("\n=== 测试各种请求格式 ===")
    
    test_cases = [
        {
            "name": "缺少train_number字段",
            "data": {
                "origin": "北京",
                "destination": "上海"
            }
        },
        {
            "name": "缺少origin字段", 
            "data": {
                "train_number": "G101",
                "destination": "上海"
            }
        },
        {
            "name": "缺少destination字段",
            "data": {
                "train_number": "G101",
                "origin": "北京"
            }
        },
        {
            "name": "字段名错误 - 使用train_no而不是train_number",
            "data": {
                "train_no": "G101",
                "origin": "北京", 
                "destination": "上海"
            }
        },
        {
            "name": "空字符串值",
            "data": {
                "train_number": "",
                "origin": "",
                "destination": ""
            }
        }
    ]
    
    url = "http://localhost:8000/api/get-route-info"
    headers = {"Content-Type": "application/json"}
    
    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        print(f"请求数据: {json.dumps(test_case['data'], ensure_ascii=False)}")
        
        try:
            response = requests.post(url, headers=headers, json=test_case['data'])
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 422:
                error_detail = response.json()
                print(f"验证错误: {json.dumps(error_detail, ensure_ascii=False, indent=2)}")
            elif response.status_code == 200:
                print("意外成功!")
                
        except Exception as e:
            print(f"请求异常: {e}")

if __name__ == "__main__":
    print("开始调试API请求...")
    
    # 测试正常请求
    test_api_endpoint()
    test_stations_endpoint()
    
    # 测试各种异常请求
    test_malformed_requests()
    
    print("\n调试完成!") 