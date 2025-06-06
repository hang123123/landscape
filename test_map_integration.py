#!/usr/bin/env python3
"""
地图功能集成测试
测试火车站点API和地图显示功能
"""

import requests
import json
import asyncio
from ai_client import AlibabaAIClient

BASE_URL = "http://localhost:8000"

async def test_route_stations_api():
    """测试获取火车站点API"""
    print("🗺️ 测试火车站点API...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/get-route-stations", 
            headers={"Content-Type": "application/json"},
            json={
                "train_number": "G1033",
                "origin": "北京",
                "destination": "上海"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                stations_data = data["data"]
                print("✅ API调用成功")
                print(f"📊 车次信息: {stations_data.get('train_info', {})}")
                print(f"🚉 站点数量: {len(stations_data.get('stations', []))}")
                
                # 打印前3个站点信息
                stations = stations_data.get('stations', [])
                for i, station in enumerate(stations[:3]):
                    print(f"   站点{i+1}: {station['name']} - 坐标({station['longitude']}, {station['latitude']})")
                
                return stations_data
            else:
                print(f"❌ API返回错误: {data.get('message')}")
                return None
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None

async def test_ai_client_directly():
    """直接测试AI客户端的站点获取功能"""
    print("\n🤖 测试AI客户端站点获取...")
    
    try:
        ai_client = AlibabaAIClient()
        train_info = {
            "train_no": "G1033",
            "from_station": "北京",
            "to_station": "上海"
        }
        
        stations_data = await ai_client.get_route_stations(train_info)
        
        if stations_data:
            print("✅ AI客户端调用成功")
            print(f"📊 列车信息: {stations_data.get('train_info', {})}")
            
            stations = stations_data.get('stations', [])
            print(f"🚉 总站点数: {len(stations)}")
            
            # 验证坐标数据
            valid_coords = 0
            for station in stations:
                lng = station.get('longitude', 0)
                lat = station.get('latitude', 0)
                if 70 < lng < 140 and 10 < lat < 60:  # 中国境内坐标范围
                    valid_coords += 1
            
            print(f"📍 有效坐标数: {valid_coords}/{len(stations)}")
            
            # 打印详细站点信息
            print("\n🚉 站点详情:")
            for station in stations:
                print(f"   {station['sequence']}. {station['name']}")
                print(f"      到达: {station['arrival_time']} | 发车: {station['departure_time']}")
                print(f"      坐标: ({station['longitude']}, {station['latitude']})")
                print(f"      景点: {', '.join(station.get('attractions', [])[:2])}")
                print(f"      美食: {', '.join(station.get('local_food', [])[:2])}")
                print()
            
            return stations_data
        else:
            print("❌ AI客户端返回空数据")
            return None
            
    except Exception as e:
        print(f"❌ AI客户端异常: {e}")
        return None

def test_coordinate_validation(stations_data):
    """测试坐标数据有效性"""
    print("📍 验证坐标数据...")
    
    if not stations_data or 'stations' not in stations_data:
        print("❌ 没有站点数据可验证")
        return False
    
    stations = stations_data['stations']
    issues = []
    
    for station in stations:
        lng = station.get('longitude', 0)
        lat = station.get('latitude', 0)
        
        # 检查坐标范围（中国境内）
        if not (70 < lng < 140):
            issues.append(f"{station['name']}: 经度异常 ({lng})")
        
        if not (10 < lat < 60):
            issues.append(f"{station['name']}: 纬度异常 ({lat})")
        
        # 检查必要字段
        required_fields = ['sequence', 'name', 'arrival_time', 'departure_time']
        for field in required_fields:
            if not station.get(field):
                issues.append(f"{station['name']}: 缺少字段 {field}")
    
    if issues:
        print("⚠️ 发现数据问题:")
        for issue in issues[:5]:  # 只显示前5个问题
            print(f"   - {issue}")
        if len(issues) > 5:
            print(f"   - 还有 {len(issues) - 5} 个问题...")
        return False
    else:
        print("✅ 所有坐标数据验证通过")
        return True

def generate_map_test_html(stations_data):
    """生成地图测试HTML文件"""
    print("\n🌐 生成地图测试文件...")
    
    if not stations_data:
        print("❌ 没有站点数据，无法生成测试文件")
        return
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>火车沿途站点地图测试</title>
    <script type="text/javascript" src="https://webapi.amap.com/maps?v=2.0&key=f3c5c85b9b6b5cc3c5e0b8b6b9b6b5cc&plugin=AMap.Scale,AMap.ToolBar,AMap.InfoWindow"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        #container {{ width: 100%; height: 600px; border: 1px solid #ccc; }}
        .info {{ margin-bottom: 20px; }}
        .station-info {{ background: #f5f5f5; padding: 10px; margin: 5px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>🚄 {stations_data['train_info']['train_no']} 次列车路线图</h1>
    <div class="info">
        <p><strong>起点:</strong> {stations_data['train_info']['from_station']}</p>
        <p><strong>终点:</strong> {stations_data['train_info']['to_station']}</p>
        <p><strong>总里程:</strong> {stations_data['train_info'].get('total_distance', 'N/A')}</p>
        <p><strong>总时长:</strong> {stations_data['train_info'].get('total_time', 'N/A')}</p>
    </div>
    
    <div id="container"></div>
    
    <h2>📍 站点列表</h2>
    {''.join([f'''
    <div class="station-info">
        <strong>{station['sequence']}. {station['name']}</strong> ({station['city']})
        <br>到达: {station['arrival_time']} | 发车: {station['departure_time']} | 停车: {station['stop_duration']}
        <br>坐标: ({station['longitude']}, {station['latitude']})
        <br>景点: {', '.join(station.get('attractions', []))}
        <br>美食: {', '.join(station.get('local_food', []))}
    </div>
    ''' for station in stations_data['stations']])}
    
    <script>
        const stationsData = {json.dumps(stations_data, ensure_ascii=False, indent=2)};
        
        // 计算地图中心点
        const stations = stationsData.stations;
        const centerLat = stations.reduce((sum, station) => sum + station.latitude, 0) / stations.length;
        const centerLng = stations.reduce((sum, station) => sum + station.longitude, 0) / stations.length;
        
        // 创建地图
        const map = new AMap.Map('container', {{
            zoom: 6,
            center: [centerLng, centerLat],
            mapStyle: 'amap://styles/normal'
        }});
        
        // 添加控件
        map.addControl(new AMap.Scale());
        map.addControl(new AMap.ToolBar());
        
        // 绘制路线
        const linePoints = stations.map(station => [station.longitude, station.latitude]);
        const polyline = new AMap.Polyline({{
            path: linePoints,
            strokeColor: '#FF6B6B',
            strokeWeight: 4,
            strokeOpacity: 0.8
        }});
        map.add(polyline);
        
        // 添加站点标记
        stations.forEach((station, index) => {{
            const marker = new AMap.Marker({{
                position: [station.longitude, station.latitude],
                title: station.name
            }});
            
            const infoWindow = new AMap.InfoWindow({{
                content: `
                    <div style="padding: 10px;">
                        <h3>${{station.sequence}}. ${{station.name}}</h3>
                        <p><strong>到达:</strong> ${{station.arrival_time}}</p>
                        <p><strong>发车:</strong> ${{station.departure_time}}</p>
                        <p><strong>停车:</strong> ${{station.stop_duration}}</p>
                        <p><strong>景点:</strong> ${{station.attractions.join(', ')}}</p>
                        <p><strong>美食:</strong> ${{station.local_food.join(', ')}}</p>
                    </div>
                `
            }});
            
            marker.on('click', () => {{
                infoWindow.open(map, marker.getPosition());
            }});
            
            map.add(marker);
        }});
        
        // 自适应显示
        map.setFitView(null, false, [50, 50, 50, 50]);
    </script>
</body>
</html>
    """
    
    try:
        with open('test_map.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("✅ 测试文件已生成: test_map.html")
        print("   用浏览器打开此文件可查看地图效果")
    except Exception as e:
        print(f"❌ 生成测试文件失败: {e}")

async def main():
    """主测试函数"""
    print("🗺️ 火车沿途风景 - 地图功能集成测试")
    print("=" * 50)
    
    # 测试API端点
    stations_data = await test_route_stations_api()
    
    # 如果API测试失败，直接测试AI客户端
    if not stations_data:
        stations_data = await test_ai_client_directly()
    
    # 验证数据质量
    if stations_data:
        test_coordinate_validation(stations_data)
        generate_map_test_html(stations_data)
    
    print("\n" + "=" * 50)
    print("✅ 测试完成")
    
    if stations_data:
        print("📋 测试结果摘要:")
        print(f"   - 车次: {stations_data['train_info']['train_no']}")
        print(f"   - 站点数: {len(stations_data['stations'])}")
        print(f"   - 起终点: {stations_data['train_info']['from_station']} → {stations_data['train_info']['to_station']}")
        print("   - 生成了 test_map.html 测试文件")
    else:
        print("❌ 测试失败，请检查服务配置")

if __name__ == "__main__":
    asyncio.run(main()) 