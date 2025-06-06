#!/usr/bin/env python3
"""
火车沿途风景应用 - 主应用程序
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Optional
import os
import logging
import json
from dotenv import load_dotenv

from ai_client import ai_client
from image_service import image_service

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 获取环境变量
AMAP_API_KEY = os.getenv("AMAP_API_KEY", "")

app = FastAPI(
    title="火车沿途风景 API",
    description="提供火车旅行路线规划和沿途景点推荐服务",
    version="1.0.0"
)

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

# 请求模型
class TrainSearchRequest(BaseModel):
    origin: str
    destination: str
    departure_date: str

class RouteInfoRequest(BaseModel):
    train_number: str
    origin: str
    destination: str

class RouteStationsRequest(BaseModel):
    train_number: str
    origin: str
    destination: str

# 根路径 - 返回主页
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """返回主页HTML"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="主页文件未找到")

# 图片测试页面
@app.get("/test-images", response_class=HTMLResponse)
async def test_images():
    """返回图片测试页面"""
    try:
        with open("test_images.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="图片测试页面未找到")

# 高德地图测试页面
@app.get("/test_amap.html", response_class=HTMLResponse)
async def test_amap():
    """返回高德地图测试页面"""
    try:
        with open("test_amap.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="高德地图测试页面未找到")

# 主页面地图调试页面
@app.get("/debug_map_mainpage.html", response_class=HTMLResponse)
async def debug_map_mainpage():
    """返回主页面地图调试页面"""
    try:
        with open("debug_map_mainpage.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="主页面地图调试页面未找到")

# SelectTrain流程调试页面
@app.get("/debug_selecttrain.html", response_class=HTMLResponse)
async def debug_selecttrain():
    """返回SelectTrain流程调试页面"""
    try:
        with open("debug_selecttrain.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="SelectTrain调试页面未找到")

# API路由
@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    try:
        # 检查AI客户端状态
        ai_status = "connected" if ai_client else "disconnected"
        
        # 检查图片服务状态
        image_status = "connected" if image_service else "disconnected"
        
        # 检查高德地图API密钥状态
        amap_status = "configured" if AMAP_API_KEY else "not_configured"
        
        return {
            "status": "healthy",
            "ai_client": ai_status,
            "image_service": image_status,
            "amap_service": amap_status,
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "version": "1.0.0"
        }

@app.get("/api/config/map")
async def get_map_config():
    """获取地图配置信息"""
    try:
        return {
            "success": True,
            "amap_api_key": AMAP_API_KEY,
            "has_key": bool(AMAP_API_KEY)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "amap_api_key": "",
            "has_key": False
        }

@app.post("/api/search-trains")
async def search_trains(request: TrainSearchRequest):
    """搜索火车车次"""
    try:
        # 使用AI客户端搜索车次
        logger.info(f"搜索火车票: {request.origin} -> {request.destination}, 日期: {request.departure_date}")
        
        # 调用AI客户端获取车次信息
        train_data = await ai_client.search_trains(
            origin=request.origin,
            destination=request.destination,
            departure_date=request.departure_date
        )
        
        # 打印完整的原始车次数据
        logger.info("=== 原始车次数据结构 ===")
        logger.info(f"数据类型: {type(train_data)}")
        logger.info(f"数据键: {list(train_data.keys()) if isinstance(train_data, dict) else 'Not a dict'}")
        logger.info(f"完整原始数据: {json.dumps(train_data, ensure_ascii=False, indent=2)}")
        logger.info("=== 原始车次数据结束 ===")
        
        # 打印详细的车次信息
        logger.info("=== 车次搜索结果解析 ===")
        logger.info(f"查询路线: {request.origin} -> {request.destination}")
        logger.info(f"出发日期: {request.departure_date}")
        
        # 处理不同的数据格式
        if isinstance(train_data, list):
            # AI客户端直接返回列表
            trains = train_data
            logger.info(f"AI客户端返回列表格式，找到车次数量: {len(trains)}")
        elif isinstance(train_data, dict) and 'trains' in train_data:
            # AI客户端返回字典格式
            trains = train_data['trains']
            logger.info(f"AI客户端返回字典格式，找到车次数量: {len(trains)}")
        else:
            logger.warning("未知的数据格式")
            trains = []
            
        if trains:
            logger.info("--- 车次详情 ---")
            for i, train in enumerate(trains, 1):
                logger.info(f"车次 {i} 完整数据: {json.dumps(train, ensure_ascii=False, indent=2)}")
                logger.info(f"车次 {i}: {train.get('train_number', 'N/A')}")
                logger.info(f"  类型: {train.get('train_type', 'N/A')}")
                logger.info(f"  出发时间: {train.get('departure_time', 'N/A')}")
                logger.info(f"  到达时间: {train.get('arrival_time', 'N/A')}")
                logger.info(f"  行程时长: {train.get('duration', 'N/A')}")
                logger.info(f"  票价: {train.get('price', 'N/A')}")
                logger.info("  " + "="*30)
        else:
            logger.warning("没有找到车次数据")
            if isinstance(train_data, dict):
                logger.info(f"可用字段: {list(train_data.keys())}")
        logger.info("=== 车次搜索解析结束 ===")
        
        return {
            "status": "success", 
            "trains": trains,
            "count": len(trains)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索车次失败: {str(e)}")

@app.post("/api/get-route-info")
async def get_route_info(request: RouteInfoRequest):
    """获取路线信息和沿途景点"""
    try:
        # 添加详细的请求日志
        logger.info(f"接收到get_route_info请求")
        logger.info(f"请求类型: {type(request)}")
        logger.info(f"请求内容: train_number={getattr(request, 'train_number', 'MISSING')}, origin={getattr(request, 'origin', 'MISSING')}, destination={getattr(request, 'destination', 'MISSING')}")
        
        logger.info(f"获取路线信息: {request.train_number} {request.origin} -> {request.destination}")
        
        # 构建train_info字典
        train_info = {
            "train_no": request.train_number,
            "from_station": request.origin,
            "to_station": request.destination
        }
        
        logger.info(f"调用AI客户端获取路线信息，参数: {train_info}")
        
        # 添加AI客户端调用前的详细日志
        logger.info("=== 准备调用AI客户端 get_route_recommendations ===")
        logger.info(f"AI客户端状态: {ai_client is not None}")
        logger.info(f"传入参数类型: {type(train_info)}")
        logger.info(f"传入参数内容: {json.dumps(train_info, ensure_ascii=False)}")
        
        try:
            # 使用AI客户端获取路线信息
            route_data = await ai_client.get_route_recommendations(train_info)
            logger.info("=== AI客户端调用成功 ===")
        except Exception as e:
            logger.error(f"=== AI客户端调用失败 ===: {e}")
            raise e
        
        logger.info(f"成功获取路线信息: {type(route_data)}")
        logger.info(f"返回数据为空: {route_data is None}")
        logger.info(f"返回数据长度: {len(route_data) if hasattr(route_data, '__len__') else 'N/A'}")
        
        # 打印完整的原始路线数据
        logger.info("=== 原始路线数据结构 ===")
        logger.info(f"数据类型: {type(route_data)}")
        logger.info(f"数据键: {list(route_data.keys()) if isinstance(route_data, dict) else 'Not a dict'}")
        logger.info(f"完整原始数据: {json.dumps(route_data, ensure_ascii=False, indent=2)}")
        logger.info("=== 原始路线数据结束 ===")
        
        # 打印详细的路线信息
        logger.info("=== 路线详细信息解析 ===")
        if 'route_info' in route_data:
            route_info = route_data['route_info']
            logger.info(f"车次: {route_info.get('train_no', 'N/A')}")
            logger.info(f"起始站: {route_info.get('from_station', 'N/A')}")
            logger.info(f"终点站: {route_info.get('to_station', 'N/A')}")
            logger.info(f"行程时间: {route_info.get('travel_time', 'N/A')}")
        else:
            logger.warning("缺少 'route_info' 字段")
        
        if 'attractions' in route_data:
            logger.info(f"沿途城市数量: {len(route_data['attractions'])}")
            for i, attraction in enumerate(route_data['attractions'], 1):
                logger.info(f"城市 {i} 完整数据: {json.dumps(attraction, ensure_ascii=False, indent=2)}")
                logger.info(f"城市 {i}: {attraction.get('city', 'N/A')}")
                logger.info(f"  描述: {attraction.get('description', 'N/A')}")
                
                scenic_spots = attraction.get('scenic_spots', [])
                if scenic_spots:
                    logger.info(f"  景点: {', '.join(scenic_spots) if isinstance(scenic_spots, list) else scenic_spots}")
                else:
                    logger.info(f"  景点: 无")
                
                local_food = attraction.get('local_food', [])
                if local_food:
                    logger.info(f"  美食: {', '.join(local_food) if isinstance(local_food, list) else local_food}")
                else:
                    logger.info(f"  美食: 无")
        else:
            logger.warning("缺少 'attractions' 字段")
        
        if 'travel_tips' in route_data:
            logger.info(f"旅行贴士数量: {len(route_data['travel_tips'])}")
            for i, tip in enumerate(route_data['travel_tips'], 1):
                logger.info(f"贴士 {i}: {tip}")
        else:
            logger.warning("缺少 'travel_tips' 字段")
        logger.info("=== 路线信息解析结束 ===")
        
        # 为景点和美食添加图片URL
        if 'attractions' in route_data:
            enhanced_attractions = []
            for attraction in route_data['attractions']:
                enhanced_attraction = {
                    'city': attraction['city'],
                    'description': attraction['description'],
                    'scenic_spots': [],
                    'local_food': []
                }
                
                # 为景点添加图片
                for i, spot in enumerate(attraction['scenic_spots']):
                    image_url = image_service.get_attraction_image(
                        spot, attraction['city'], i
                    )
                    enhanced_attraction['scenic_spots'].append({
                        'name': spot,
                        'image': image_url
                    })
                
                # 为美食添加图片
                for i, food in enumerate(attraction['local_food']):
                    image_url = image_service.get_food_image(
                        food, attraction['city'], i
                    )
                    enhanced_attraction['local_food'].append({
                        'name': food,
                        'image': image_url
                    })
                
                enhanced_attractions.append(enhanced_attraction)
            
            route_data['attractions'] = enhanced_attractions
        
        # 统一返回格式
        return {
            "success": True,
            "data": route_data,
            "message": "路线信息获取成功"
        }
        
    except Exception as e:
        logger.error(f"获取路线信息时出错: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取路线信息失败: {str(e)}")

@app.get("/api/images/attractions/{city}")
async def get_attraction_images(city: str, count: int = 4):
    """获取特定城市的景点图片"""
    try:
        images = []
        for i in range(count):
            image_url = image_service.get_attraction_image("景点", city, i)
            images.append({
                "url": image_url,
                "alt": f"{city}景点{i+1}"
            })
        
        return {
            "status": "success",
            "city": city,
            "images": images
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取景点图片失败: {str(e)}")

@app.get("/api/images/foods/{city}")
async def get_food_images(city: str, count: int = 4):
    """获取特定城市的美食图片"""
    try:
        images = []
        for i in range(count):
            image_url = image_service.get_food_image("美食", city, i)
            images.append({
                "url": image_url,
                "alt": f"{city}美食{i+1}"
            })
        
        return {
            "status": "success",
            "city": city,
            "images": images
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取美食图片失败: {str(e)}")

@app.get("/api/images/random")
async def get_random_images(category: str = "attraction", count: int = 8):
    """获取随机图片"""
    try:
        if category not in ["attraction", "food"]:
            raise HTTPException(status_code=400, detail="类别必须是 'attraction' 或 'food'")
        
        images = image_service.get_random_images(category, count)
        
        return {
            "status": "success",
            "category": category,
            "images": [{"url": url, "alt": f"{category}_{i}"} for i, url in enumerate(images)]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取随机图片失败: {str(e)}")

@app.post("/api/images/batch")
async def get_images_batch(attractions: List[Dict]):
    """批量获取图片URL"""
    try:
        result = image_service.get_image_urls_batch(attractions)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量获取图片失败: {str(e)}")

@app.post("/api/get-route-stations")
async def get_route_stations(request: RouteStationsRequest):
    """获取路线站点信息（用于地图显示）"""
    try:
        # 添加详细的请求日志
        logger.info(f"接收到get_route_stations请求")
        logger.info(f"请求类型: {type(request)}")
        logger.info(f"请求内容: train_number={getattr(request, 'train_number', 'MISSING')}, origin={getattr(request, 'origin', 'MISSING')}, destination={getattr(request, 'destination', 'MISSING')}")
        
        logger.info(f"获取站点信息: {request.train_number} {request.origin} -> {request.destination}")
        
        # 构建请求数据
        train_info = {
            "train_no": request.train_number,
            "from_station": request.origin,
            "to_station": request.destination
        }
        
        logger.info(f"调用AI客户端获取站点数据，参数: {train_info}")
        
        # 添加AI客户端调用前的详细日志
        logger.info("=== 准备调用AI客户端 get_route_stations ===")
        logger.info(f"AI客户端状态: {ai_client is not None}")
        logger.info(f"传入参数类型: {type(train_info)}")
        logger.info(f"传入参数内容: {json.dumps(train_info, ensure_ascii=False)}")
        
        try:
            # 调用AI客户端获取站点数据
            stations_data = await ai_client.get_route_stations(train_info)
            logger.info("=== AI客户端调用成功 ===")
        except Exception as e:
            logger.error(f"=== AI客户端调用失败 ===: {e}")
            raise e
        
        logger.info(f"成功获取站点数据: {type(stations_data)}")
        logger.info(f"返回数据为空: {stations_data is None}")
        logger.info(f"返回数据长度: {len(stations_data) if hasattr(stations_data, '__len__') else 'N/A'}")
        
        # 打印完整的原始数据结构
        logger.info("=== 原始12306数据结构 ===")
        logger.info(f"数据类型: {type(stations_data)}")
        logger.info(f"数据键: {list(stations_data.keys()) if isinstance(stations_data, dict) else 'Not a dict'}")
        logger.info(f"完整原始数据: {json.dumps(stations_data, ensure_ascii=False, indent=2)}")
        logger.info("=== 原始数据结束 ===")
        
        # 打印详细的站点信息
        logger.info("=== 12306站点详细信息解析 ===")
        if 'train_info' in stations_data:
            train_info_data = stations_data['train_info']
            logger.info(f"车次: {train_info_data.get('train_no', 'N/A')}")
            logger.info(f"始发站: {train_info_data.get('from_station', 'N/A')}")
            logger.info(f"终点站: {train_info_data.get('to_station', 'N/A')}")
            logger.info(f"总里程: {train_info_data.get('total_distance', 'N/A')}")
            logger.info(f"总时长: {train_info_data.get('total_time', 'N/A')}")
        else:
            logger.warning("缺少 'train_info' 字段")
        
        if 'stations' in stations_data:
            stations = stations_data['stations']
            logger.info(f"停靠站点数量: {len(stations)}")
            logger.info(f"站点数据类型: {type(stations)}")
            logger.info("--- 详细停靠信息 ---")
            for idx, station in enumerate(stations):
                logger.info(f"第{idx+1}个站点数据类型: {type(station)}")
                logger.info(f"第{idx+1}个站点完整数据: {json.dumps(station, ensure_ascii=False, indent=2)}")
                logger.info(f"站序 {station.get('sequence', 'N/A')}: {station.get('name', 'N/A')}")
                logger.info(f"  所在城市: {station.get('city', 'N/A')}")
                logger.info(f"  到达时间: {station.get('arrival_time', 'N/A')}")
                logger.info(f"  发车时间: {station.get('departure_time', 'N/A')}")
                logger.info(f"  停车时长: {station.get('stop_duration', 'N/A')}")
                logger.info(f"  经纬度: ({station.get('longitude', 'N/A')}, {station.get('latitude', 'N/A')})")
                logger.info(f"  是否主要站点: {station.get('is_major', False)}")
                
                attractions = station.get('attractions', [])
                if attractions:
                    logger.info(f"  周边景点: {', '.join(attractions) if isinstance(attractions, list) else attractions}")
                else:
                    logger.info(f"  周边景点: 无")
                
                local_food = station.get('local_food', [])
                if local_food:
                    logger.info(f"  特色美食: {', '.join(local_food) if isinstance(local_food, list) else local_food}")
                else:
                    logger.info(f"  特色美食: 无")
                logger.info("  " + "="*50)
        else:
            logger.warning("缺少 'stations' 字段")
            logger.info(f"可用字段: {list(stations_data.keys()) if isinstance(stations_data, dict) else '数据不是字典格式'}")
        logger.info("=== 12306站点信息解析结束 ===")
        
        return {
            "success": True,
            "data": stations_data,
            "message": "站点信息获取成功"
        }
        
    except Exception as e:
        logger.error(f"获取站点信息时出错: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取站点信息失败: {str(e)}")

# 异常处理
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """404错误处理"""
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": "请求的资源未找到",
            "path": str(request.url)
        }
    )

@app.exception_handler(500)
async def server_error_handler(request: Request, exc: HTTPException):
    """500错误处理"""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "服务器内部错误",
            "path": str(request.url)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 