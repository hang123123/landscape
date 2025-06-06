import json
import asyncio
from typing import Dict, List, Any, Optional
import httpx
import os
from dotenv import load_dotenv
from dashscope import Application
from http import HTTPStatus

load_dotenv()

class AlibabaAIClient:
    """阿里百炼API客户端 - 使用Application.call方式"""
    
    def __init__(self):
        self.api_key = os.getenv("ALIBABA_DASHSCOPE_API_KEY")
        self.app_id = os.getenv("ALIBABA_DASHSCOPE_APP_ID")
        
        if not self.api_key:
            print("⚠️  未找到阿里百炼API密钥，将使用模拟数据")
        if not self.app_id:
            print("⚠️  未找到阿里百炼应用ID，将使用模拟数据")

    async def get_route_recommendations(self, train_info: Dict[str, Any]) -> Dict[str, Any]:
        """根据火车信息获取沿途推荐"""
        try:
            # 构建提示词
            prompt = self._build_route_prompt(train_info)
            
            # 如果没有配置API密钥或应用ID，使用模拟数据
            if not self.api_key or not self.app_id:
                return self._get_mock_route_data(train_info)
            
            # 调用阿里百炼API
            response_text = await self._call_api(prompt)
            
            # 解析响应
            return self._parse_response(response_text, train_info)
            
        except Exception as e:
            print(f"获取路线推荐时出错: {e}")
            return self._get_mock_route_data(train_info)

    def _build_route_prompt(self, train_info: Dict[str, Any]) -> str:
        """构建发送给AI的提示词"""
        from_station = train_info.get('from_station', '未知')
        to_station = train_info.get('to_station', '未知')
        train_no = train_info.get('train_no', '未知')
        
        prompt = f"""请为我推荐从{from_station}到{to_station}的{train_no}次列车沿途的风景名胜和特色美食。

要求：
1. 推荐3-5个沿途主要城市或景点
2. 每个地点包括：景点名称、特色美食、简短描述
3. 返回JSON格式，结构如下：
{{
  "route_info": {{
    "train_no": "{train_no}",
    "from_station": "{from_station}",
    "to_station": "{to_station}",
    "travel_time": "约X小时"
  }},
  "attractions": [
    {{
      "city": "城市名",
      "scenic_spots": ["景点1", "景点2"],
      "local_food": ["美食1", "美食2"],
      "description": "简短描述"
    }}
  ],
  "travel_tips": ["贴士1", "贴士2"]
}}

请确保返回有效的JSON格式。"""

        return prompt

    async def _call_api(self, prompt: str) -> str:
        """调用阿里百炼API"""
        try:
            # 使用Application.call方式调用
            response = Application.call(
                api_key=self.api_key,
                app_id=self.app_id,
                prompt=prompt
            )
            
            # 检查响应状态
            if response.status_code != HTTPStatus.OK:
                print(f"百炼API错误: {response.status_code} {getattr(response, 'message', '')}")
                raise Exception(f"API调用失败: {response.status_code}")
            
            # 提取回复文本
            reply = getattr(response.output, 'text', '') if hasattr(response, 'output') else ''
            reply = reply.replace('*', '')  # 清理格式字符
            
            return reply
            
        except Exception as e:
            print(f"调用阿里百炼API失败: {e}")
            raise

    def _parse_response(self, response_text: str, train_info: Dict[str, Any]) -> Dict[str, Any]:
        """解析AI响应"""
        try:
            # 尝试直接解析JSON
            if response_text.strip().startswith('{'):
                return json.loads(response_text)
            
            # 如果不是JSON格式，尝试提取JSON部分
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # 如果无法解析为JSON，构建基本结构
            return self._create_basic_structure(response_text, train_info)
            
        except json.JSONDecodeError:
            return self._create_basic_structure(response_text, train_info)

    def _create_basic_structure(self, text: str, train_info: Dict[str, Any]) -> Dict[str, Any]:
        """当无法解析JSON时，创建基本结构"""
        return {
            "route_info": {
                "train_no": train_info.get('train_no', '未知'),
                "from_station": train_info.get('from_station', '未知'),
                "to_station": train_info.get('to_station', '未知'),
                "travel_time": "约4-8小时"
            },
            "attractions": [
                {
                    "city": "沿途城市",
                    "scenic_spots": ["自然风光", "历史古迹"],
                    "local_food": ["地方特色", "传统小吃"],
                    "description": text[:200] + "..." if len(text) > 200 else text
                }
            ],
            "travel_tips": [
                "提前查看天气情况",
                "准备舒适的旅行装备",
                "注意列车时刻表"
            ]
        }

    def _get_mock_route_data(self, train_info: Dict[str, Any]) -> Dict[str, Any]:
        """模拟数据（当API不可用时使用）"""
        from_station = train_info.get('from_station', '北京')
        to_station = train_info.get('to_station', '上海')
        train_no = train_info.get('train_no', 'G1')
        
        mock_data = {
            "route_info": {
                "train_no": train_no,
                "from_station": from_station,
                "to_station": to_station,
                "travel_time": "约4-6小时"
            },
            "attractions": [
                {
                    "city": "徐州",
                    "scenic_spots": ["云龙湖", "徐州博物馆", "彭祖园"],
                    "local_food": ["徐州烧饼", "羊方藏鱼", "蜜三刀"],
                    "description": "徐州是历史文化名城，有着丰富的汉文化遗存和美丽的自然风光。"
                },
                {
                    "city": "南京",
                    "scenic_spots": ["中山陵", "明孝陵", "夫子庙"],
                    "local_food": ["盐水鸭", "鸭血粉丝汤", "汤包"],
                    "description": "六朝古都南京，历史悠久，文化底蕴深厚，是著名的旅游城市。"
                },
                {
                    "city": "苏州",
                    "scenic_spots": ["拙政园", "虎丘", "平江路"],
                    "local_food": ["阳澄湖大闸蟹", "苏式月饼", "糖醋排骨"],
                    "description": "苏州园林甲天下，是中国古典园林的代表，素有人间天堂的美誉。"
                }
            ],
            "travel_tips": [
                "建议提前预订酒店，特别是旅游旺季",
                "携带身份证件，部分景点需要实名预约",
                "注意天气变化，准备合适的衣物",
                "下载离线地图，避免在没有网络时迷路"
            ]
        }
        
        return mock_data

    async def search_trains(self, origin: str, destination: str, departure_date: str) -> List[Dict]:
        """搜索车次信息 - 使用百炼大模型"""
        try:
            # 如果没有配置API密钥或应用ID，使用模拟数据
            if not self.api_key or not self.app_id:
                return self._get_mock_trains()
            
            # 构建查询车次的提示词
            prompt = f"""请帮我查询{departure_date}从{origin}到{destination}的火车车次信息。

要求：
1. 列出3-8个不同时间段的车次选项
2. 包含高铁、动车、普通列车等不同类型
3. 返回JSON格式，包含以下字段：
   - train_number: 车次号
   - departure_time: 发车时间 
   - arrival_time: 到达时间
   - duration: 运行时长
   - price: 票价
   - train_type: 车型(如：高速动车、动车、普快等)

返回格式：
[
  {{
    "train_number": "G1",
    "departure_time": "08:30",
    "arrival_time": "14:25",
    "duration": "5小时55分",
    "price": "553元",
    "train_type": "高速动车"
  }}
]

请确保返回有效的JSON数组格式。"""

            # 调用阿里百炼API
            response_text = await self._call_api(prompt)
            
            # 解析响应
            trains_data = self._extract_json_from_response(response_text)
            return trains_data if trains_data and isinstance(trains_data, list) else self._get_mock_trains()
            
        except Exception as e:
            print(f"搜索车次时出错: {e}")
            return self._get_mock_trains()
    
    def _extract_json_from_response(self, response: str) -> Any:
        """从AI响应中提取JSON数据"""
        try:
            # 尝试直接解析
            if response.strip().startswith('[') or response.strip().startswith('{'):
                return json.loads(response)
        except json.JSONDecodeError:
            pass
            
        # 如果直接解析失败，尝试提取JSON块
        import re
        
        # 尝试提取 ```json...``` 块
        json_pattern = r'```json\s*(.*?)\s*```'
        match = re.search(json_pattern, response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        
        # 尝试查找数组或对象
        for pattern in [r'\[.*\]', r'\{.*\}']:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
        
        return None
    
    def _get_mock_trains(self) -> List[Dict]:
        """模拟车次数据"""
        return [
            {
                "train_number": "G1033",
                "departure_time": "08:30",
                "arrival_time": "14:25",
                "duration": "5小时55分",
                "price": "553元",
                "train_type": "高速动车"
            },
            {
                "train_number": "G1035",
                "departure_time": "09:15",
                "arrival_time": "15:10",
                "duration": "5小时55分",
                "price": "553元",
                "train_type": "高速动车"
            },
            {
                "train_number": "D3563",
                "departure_time": "10:20",
                "arrival_time": "17:45",
                "duration": "7小时25分",
                "price": "350元",
                "train_type": "动车"
            },
            {
                "train_number": "K1021",
                "departure_time": "12:30",
                "arrival_time": "05:40+1",
                "duration": "17小时10分",
                "price": "165元",
                "train_type": "快速"
            }
        ]
    
    def _get_mock_route(self) -> Dict:
        """模拟路线数据"""
        return {
            "stations": [
                {
                    "name": "北京南站",
                    "attractions": [
                        {
                            "name": "天安门广场",
                            "name_en": "Tiananmen Square",
                            "description": "世界最大的城市广场，中华人民共和国的象征",
                            "image": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=400"
                        },
                        {
                            "name": "故宫博物院",
                            "name_en": "Forbidden City",
                            "description": "明清两代皇家宫殿，世界文化遗产",
                            "image": "https://images.unsplash.com/photo-1537495329792-41ae41ad3bf0?w=400"
                        },
                        {
                            "name": "天坛公园",
                            "name_en": "Temple of Heaven",
                            "description": "明清皇帝祭天的场所，建筑艺术瑰宝",
                            "image": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400"
                        }
                    ],
                    "foods": [
                        {
                            "name": "北京烤鸭",
                            "name_en": "Peking Duck",
                            "description": "北京最著名的传统名菜，皮脆肉嫩，香味浓郁",
                            "image": "https://images.unsplash.com/photo-1505253668822-42074d58a7c6?w=400"
                        },
                        {
                            "name": "老北京炸酱面",
                            "name_en": "Beijing Zhajiangmian",
                            "description": "传统京味面食，酱香浓郁，配菜丰富",
                            "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400"
                        },
                        {
                            "name": "豆汁焦圈",
                            "name_en": "Douzhir & Jiaoquan",
                            "description": "地道的老北京早餐，独特的发酵豆浆配油炸面圈",
                            "image": "https://images.unsplash.com/photo-1551218808-94e220e084d2?w=400"
                        }
                    ]
                },
                {
                    "name": "天津站",
                    "attractions": [
                        {
                            "name": "天津之眼",
                            "name_en": "Tianjin Eye",
                            "description": "世界唯一建在桥上的摩天轮，俯瞰海河美景",
                            "image": "https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=400"
                        },
                        {
                            "name": "五大道",
                            "name_en": "Five Avenues",
                            "description": "天津最具特色的万国建筑博览苑",
                            "image": "https://images.unsplash.com/photo-1542640244-6fdb98c71b32?w=400"
                        },
                        {
                            "name": "古文化街",
                            "name_en": "Ancient Culture Street",
                            "description": "津门故里，体验传统文化的最佳去处",
                            "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400"
                        }
                    ],
                    "foods": [
                        {
                            "name": "狗不理包子",
                            "name_en": "Goubuli Baozi",
                            "description": "天津三绝之一，皮薄馅大，口感鲜美",
                            "image": "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=400"
                        },
                        {
                            "name": "煎饼果子",
                            "name_en": "Jianbing Guozi",
                            "description": "天津街头经典早餐，香脆可口，营养丰富",
                            "image": "https://images.unsplash.com/photo-1613564834361-9436948817d1?w=400"
                        },
                        {
                            "name": "耳朵眼炸糕",
                            "name_en": "Erduoyan Zhagao",
                            "description": "天津传统小吃，外酥内软，甜而不腻",
                            "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400"
                        }
                    ]
                },
                {
                    "name": "济南西站",
                    "attractions": [
                        {
                            "name": "趵突泉",
                            "name_en": "Baotu Spring",
                            "description": "天下第一泉，济南的象征和标志",
                            "image": "https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?w=400"
                        },
                        {
                            "name": "大明湖",
                            "name_en": "Daming Lake",
                            "description": "济南三大名胜之一，四面荷花三面柳",
                            "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
                        },
                        {
                            "name": "千佛山",
                            "name_en": "Qianfo Mountain",
                            "description": "济南三大名胜之一，佛教文化浓厚",
                            "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
                        }
                    ],
                    "foods": [
                        {
                            "name": "九转大肠",
                            "name_en": "Jiuzhuan Dachang",
                            "description": "鲁菜经典名菜，酸甜咸辣俱全，口感丰富",
                            "image": "https://images.unsplash.com/photo-1606850752749-3001794d1e66?w=400"
                        },
                        {
                            "name": "孟家扒蹄",
                            "name_en": "Mengjia Pati",
                            "description": "济南传统名菜，软烂香甜，肥而不腻",
                            "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=400"
                        },
                        {
                            "name": "济南把子肉",
                            "name_en": "Jinan Bazi Pork",
                            "description": "济南特色小吃，肥瘦相间，香而不腻",
                            "image": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400"
                        }
                    ]
                },
                {
                    "name": "上海虹桥站",
                    "attractions": [
                        {
                            "name": "外滩",
                            "name_en": "The Bund",
                            "description": "上海的标志性景观，万国建筑博览群",
                            "image": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400"
                        },
                        {
                            "name": "东方明珠",
                            "name_en": "Oriental Pearl Tower",
                            "description": "上海地标建筑，现代都市的象征",
                            "image": "https://images.unsplash.com/photo-1548919973-5cef591cdbc9?w=400"
                        },
                        {
                            "name": "豫园",
                            "name_en": "Yu Garden",
                            "description": "江南古典园林，体验传统文化的绝佳去处",
                            "image": "https://images.unsplash.com/photo-1559564484-d48d2bc1c6d6?w=400"
                        }
                    ],
                    "foods": [
                        {
                            "name": "小笼包",
                            "name_en": "Xiaolongbao",
                            "description": "上海经典点心，皮薄汁多，鲜美可口",
                            "image": "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=400"
                        },
                        {
                            "name": "生煎包",
                            "name_en": "Shengjian Bao",
                            "description": "上海传统小吃，底部煎至金黄，香脆可口",
                            "image": "https://images.unsplash.com/photo-1563379091339-03246c84d75e?w=400"
                        },
                        {
                            "name": "白切鸡",
                            "name_en": "White Cut Chicken",
                            "description": "上海家常菜，原汁原味，清淡鲜美",
                            "image": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400"
                        }
                    ]
                }
            ]
        }

    async def get_route_stations(self, train_info: Dict[str, Any]) -> Dict[str, Any]:
        """获取火车途径站点信息 - 包含地理位置等详细信息"""
        try:
            # 如果没有配置API密钥，使用模拟数据
            if not self.api_key or not self.app_id:
                return self._get_mock_stations_data(train_info)
            
            # 构建查询站点的提示词
            prompt = f"""请帮我查询{train_info.get('train_no', 'G1')}次列车从{train_info.get('from_station', '北京')}到{train_info.get('to_station', '上海')}的详细途径站点信息。

要求：
1. 列出所有途径站点的详细信息
2. 包含每个站点的经纬度坐标（用于地图标注）
3. 包含到达时间、发车时间、停车时长、站序等信息
4. 返回JSON格式，包含以下字段：

返回格式：
{{
  "train_info": {{
    "train_no": "{train_info.get('train_no', 'G1')}",
    "from_station": "{train_info.get('from_station', '北京')}",
    "to_station": "{train_info.get('to_station', '上海')}",
    "total_distance": "1318公里",
    "total_time": "5小时55分"
  }},
  "stations": [
    {{
      "sequence": 1,
      "name": "北京南站",
      "arrival_time": "始发站",
      "departure_time": "08:30",
      "stop_duration": "0分钟",
      "longitude": 116.378631,
      "latitude": 39.865689,
      "city": "北京",
      "is_major": true,
      "attractions": ["天安门广场", "故宫", "颐和园"],
      "local_food": ["北京烤鸭", "炸酱面", "豆汁"]
    }},
    {{
      "sequence": 2,
      "name": "济南西站",
      "arrival_time": "10:25",
      "departure_time": "10:27",
      "stop_duration": "2分钟",
      "longitude": 116.823834,
      "latitude": 36.671162,
      "city": "济南",
      "is_major": true,
      "attractions": ["趵突泉", "大明湖", "千佛山"],
      "local_food": ["把子肉", "甜沫", "油旋"]
    }}
  ]
}}

请确保返回有效的JSON格式，经纬度坐标要准确。"""

            # 调用阿里百炼API
            response_text = await self._call_api(prompt)
            
            # 解析响应
            stations_data = self._extract_json_from_response(response_text)
            return stations_data if stations_data and isinstance(stations_data, dict) else self._get_mock_stations_data(train_info)
            
        except Exception as e:
            print(f"获取站点信息时出错: {e}")
            return self._get_mock_stations_data(train_info)

    def _get_mock_stations_data(self, train_info: Dict[str, Any]) -> Dict[str, Any]:
        """模拟站点数据（当API不可用时使用）"""
        from_station = train_info.get('from_station', '北京')
        to_station = train_info.get('to_station', '上海')
        train_no = train_info.get('train_no', 'G1')
        
        # 根据起终点提供不同的模拟数据
        stations_data = {
            "train_info": {
                "train_no": train_no,
                "from_station": from_station,
                "to_station": to_station,
                "total_distance": "1318公里",
                "total_time": "5小时55分"
            },
            "stations": [
                {
                    "sequence": 1,
                    "name": f"{from_station}南站" if from_station == "北京" else f"{from_station}站",
                    "arrival_time": "始发站",
                    "departure_time": "08:30",
                    "stop_duration": "0分钟",
                    "longitude": 116.378631 if from_station == "北京" else 121.473701,
                    "latitude": 39.865689 if from_station == "北京" else 31.230416,
                    "city": from_station,
                    "is_major": True,
                    "attractions": self._get_city_attractions(from_station),
                    "local_food": self._get_city_food(from_station)
                },
                {
                    "sequence": 2,
                    "name": "济南西站",
                    "arrival_time": "10:25",
                    "departure_time": "10:27",
                    "stop_duration": "2分钟",
                    "longitude": 116.823834,
                    "latitude": 36.671162,
                    "city": "济南",
                    "is_major": True,
                    "attractions": ["趵突泉", "大明湖", "千佛山"],
                    "local_food": ["把子肉", "甜沫", "油旋"]
                },
                {
                    "sequence": 3,
                    "name": "徐州东站",
                    "arrival_time": "11:45",
                    "departure_time": "11:47",
                    "stop_duration": "2分钟",
                    "longitude": 117.342835,
                    "latitude": 34.435556,
                    "city": "徐州",
                    "is_major": True,
                    "attractions": ["云龙湖", "徐州博物馆", "彭祖园"],
                    "local_food": ["徐州烧饼", "羊方藏鱼", "蜜三刀"]
                },
                {
                    "sequence": 4,
                    "name": "南京南站",
                    "arrival_time": "12:35",
                    "departure_time": "12:37",
                    "stop_duration": "2分钟",
                    "longitude": 118.896805,
                    "latitude": 31.934844,
                    "city": "南京",
                    "is_major": True,
                    "attractions": ["中山陵", "明孝陵", "夫子庙"],
                    "local_food": ["盐水鸭", "鸭血粉丝汤", "汤包"]
                },
                {
                    "sequence": 5,
                    "name": "苏州北站",
                    "arrival_time": "13:15",
                    "departure_time": "13:17",
                    "stop_duration": "2分钟",
                    "longitude": 120.685417,
                    "latitude": 31.406944,
                    "city": "苏州",
                    "is_major": True,
                    "attractions": ["拙政园", "虎丘", "平江路"],
                    "local_food": ["阳澄湖大闸蟹", "苏式月饼", "糖醋排骨"]
                },
                {
                    "sequence": 6,
                    "name": f"{to_station}虹桥站" if to_station == "上海" else f"{to_station}站",
                    "arrival_time": "14:25",
                    "departure_time": "终点站",
                    "stop_duration": "0分钟",
                    "longitude": 121.319784 if to_station == "上海" else 121.473701,
                    "latitude": 31.197645 if to_station == "上海" else 31.230416,
                    "city": to_station,
                    "is_major": True,
                    "attractions": self._get_city_attractions(to_station),
                    "local_food": self._get_city_food(to_station)
                }
            ]
        }
        
        return stations_data

    def _get_city_attractions(self, city: str) -> List[str]:
        """根据城市返回主要景点"""
        attractions_map = {
            "北京": ["天安门广场", "故宫", "颐和园", "长城"],
            "上海": ["外滩", "东方明珠", "豫园", "城隍庙"],
            "南京": ["中山陵", "明孝陵", "夫子庙", "总统府"],
            "苏州": ["拙政园", "虎丘", "平江路", "留园"],
            "杭州": ["西湖", "灵隐寺", "雷峰塔", "宋城"],
            "广州": ["广州塔", "陈家祠", "白云山", "沙面岛"],
            "深圳": ["世界之窗", "欢乐谷", "大梅沙", "莲花山"],
            "武汉": ["黄鹤楼", "东湖", "归元寺", "户部巷"]
        }
        return attractions_map.get(city, ["历史古迹", "自然风光", "文化景点"])

    def _get_city_food(self, city: str) -> List[str]:
        """根据城市返回特色美食"""
        food_map = {
            "北京": ["北京烤鸭", "炸酱面", "豆汁", "驴打滚"],
            "上海": ["小笼包", "生煎包", "上海菜饭", "白切鸡"],
            "南京": ["盐水鸭", "鸭血粉丝汤", "汤包", "桂花糖芋苗"],
            "苏州": ["阳澄湖大闸蟹", "苏式月饼", "糖醋排骨", "响油鳝丝"],
            "杭州": ["西湖醋鱼", "东坡肉", "龙井虾仁", "叫化鸡"],
            "广州": ["白切鸡", "烧鹅", "肠粉", "艇仔粥"],
            "深圳": ["沙井蚝", "南澳海胆", "光明乳鸽", "客家菜"],
            "武汉": ["热干面", "豆皮", "鸭脖", "莲藕排骨汤"]
        }
        return food_map.get(city, ["地方特色", "传统小吃", "风味菜肴"])

# 创建全局AI客户端实例
ai_client = AlibabaAIClient() 