# 🤖 阿里百炼API完整配置指南

## ✅ 当前实现状态

**✅ 已完成：**
- 使用正确的 `Application.call` 方式调用阿里百炼
- 支持 API Key + App ID 配置
- 完整的错误处理和降级机制
- 模拟数据作为备选方案
- JSON响应解析和格式化

**✅ 技术实现：**
- 使用官方 `dashscope==1.20.0` SDK
- 基于您提供的示例正确实现
- 异步调用支持
- 完整的提示词工程

## 📋 配置清单

### 1. 环境依赖
```bash
pip install dashscope==1.20.0
```

### 2. 获取配置信息

#### 2.1 API Key（必需）
1. 访问：https://dashscope.console.aliyun.com/
2. 左侧菜单 → "API Key管理"
3. 点击"创建新的API Key"
4. 复制格式如：`sk-26e235b4b7e54d259b936f8b76c8a062`

#### 2.2 应用ID（必需）
1. 左侧菜单 → "我的应用"
2. 点击"创建应用" → 选择"Agent应用"
3. 填写应用信息并创建
4. 复制应用ID，格式如：`485f3c8e1d034a54a12a51984114b0f3`

### 3. 项目配置

#### 3.1 创建 .env 文件
```bash
cp env.example .env
```

#### 3.2 填写配置
编辑 `.env` 文件：
```bash
# 阿里百炼配置（必须填写）
ALIBABA_DASHSCOPE_API_KEY=sk-26e235b4b7e54d259b936f8b76c8a062
ALIBABA_DASHSCOPE_APP_ID=485f3c8e1d034a54a12a51984114b0f3

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

## 🧪 测试验证

### 1. 启动服务
```bash
python start.py
```

### 2. 健康检查
```bash
curl http://localhost:8000/api/health
```

**期望结果：**
- 未配置：`"ai_client": "using_mock_data"`
- 已配置：`"ai_client": "connected"`

### 3. 测试AI功能
```bash
curl -X POST http://localhost:8000/api/get-route-info \
  -H "Content-Type: application/json" \
  -d '{"train_number":"G1","origin":"北京南","destination":"上海虹桥"}'
```

## 🔧 技术实现详情

### AI客户端实现
```python
# ai_client.py 中的核心实现
from dashscope import Application
from http import HTTPStatus

response = Application.call(
    api_key=self.api_key,
    app_id=self.app_id, 
    prompt=prompt
)

if response.status_code != HTTPStatus.OK:
    # 错误处理
    raise Exception(f"API调用失败: {response.status_code}")

reply = getattr(response.output, 'text', '') if hasattr(response, 'output') else ''
reply = reply.replace('*', '')  # 清理格式字符
```

### 提示词工程
系统会自动构建结构化提示词：
```
请为我推荐从{起点}到{终点}的{车次}次列车沿途的风景名胜和特色美食。

要求：
1. 推荐3-5个沿途主要城市或景点
2. 每个地点包括：景点名称、特色美食、简短描述  
3. 返回JSON格式...
```

## 🛡️ 降级机制

1. **无API配置**：自动使用模拟数据
2. **API调用失败**：降级到模拟数据
3. **响应解析失败**：构建基础数据结构
4. **网络问题**：优雅降级处理

## 📊 响应格式

**标准JSON响应：**
```json
{
  "route_info": {
    "train_no": "G1",
    "from_station": "北京南", 
    "to_station": "上海虹桥",
    "travel_time": "约4-6小时"
  },
  "attractions": [
    {
      "city": "南京",
      "scenic_spots": ["中山陵", "明孝陵"],
      "local_food": ["盐水鸭", "汤包"],
      "description": "六朝古都..."
    }
  ],
  "travel_tips": ["建议提前预订酒店", "注意天气变化"]
}
```

## 🎯 使用建议

1. **开发阶段**：可以不配置API，使用模拟数据进行功能开发
2. **生产环境**：必须配置真实的API Key和App ID
3. **成本控制**：建议在阿里云控制台设置API调用限额
4. **监控日志**：注意观察API调用状态和错误信息

---

**✅ 当前状态：已完全按照您的示例实现阿里百炼API调用！** 