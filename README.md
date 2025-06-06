# 🚄 火车沿途风景 | Journey Along the Rails

一个基于AI的智能火车旅行规划平台，帮助用户发现沿途站点的美景与美食。

## ✨ 功能特点

- 🔍 **智能车次搜索** - 根据起点、终点和出发时间推荐最佳车次
- 🎯 **AI驱动推荐** - 基于阿里百炼大模型提供个性化景点和美食推荐
- 🎨 **现代化界面** - 采用Bento Grid设计风格，Apple官网级的滚动动效
- 📱 **响应式设计** - 完美适配桌面端和移动端
- 🖼️ **丰富视觉** - 集成高质量免费图片，增强视觉体验

## 🛠️ 技术栈

### 后端
- **FastAPI** - 高性能Python Web框架
- **Pydantic** - 数据验证和设置管理
- **Uvicorn** - ASGI服务器

### 前端
- **HTML5 + Tailwind CSS** - 现代化UI框架
- **Framer Motion** - 流畅动画效果
- **Font Awesome** - 专业图标库
- **Vanilla JavaScript** - 原生JS交互

### AI集成
- **阿里百炼** - 大语言模型API
- **智能推荐** - 基于自然语言处理的景点美食推荐

## 🚀 快速开始

### 1. 环境准备

确保你的系统已安装：
- Python 3.8+
- pip 包管理器

### 2. 项目安装

```bash
# 克隆项目
git clone <your-repo-url>
cd 火车沿途风景

# 安装依赖
pip install -r requirements.txt
```

### 3. 环境配置

#### 3.1 阿里百炼API Key配置

**🔑 完整配置指南请查看：[BAILIAN_CONFIG.md](BAILIAN_CONFIG.md)**

**快速配置步骤：**

**第一步：申请阿里云账号**
1. 访问 [阿里云官网](https://www.aliyun.com)
2. 注册并完成实名认证

**第二步：开通DashScope服务**
1. 登录阿里云控制台
2. 搜索"DashScope"或直接访问：https://dashscope.console.aliyun.com/
3. 点击"开通服务"并同意相关协议
4. 选择合适的计费方式（建议先开通免费试用）

**第三步：获取API Key**
1. 在DashScope控制台，点击左侧菜单"API Key管理"
2. 点击"创建新的API Key"
3. 复制生成的API Key（格式类似：sk-xxxxxxxxxxxxxxxxx）

**第四步：配置环境变量**

```bash
# 复制环境变量文件
cp env.example .env

# 编辑 .env 文件
nano .env
```

在 `.env` 文件中填入您的API Key：
```bash
# 阿里百炼API配置 - 必填
ALIBABA_DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxx

# 其他配置（可选）
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

**⚠️ 重要提醒：**
- API Key是敏感信息，请勿提交到代码仓库
- 建议设置API调用限额，避免意外消费
- 如未配置API Key，系统将自动使用模拟数据

#### 3.2 验证配置

启动应用后，访问健康检查接口验证配置：
```bash
curl http://localhost:8000/api/health
```

返回结果示例：
```json
{
  "status": "healthy",
  "ai_client": "connected",  // 已连接AI
  "version": "1.0.0"
}
```

如果显示 `"ai_client": "using_mock_data"`，表示未正确配置API Key。

#### 3.3 高德地图服务
1. 前往[高德开放平台](https://lbs.amap.com/)注册开发者账号
2. 创建应用并获取Web服务API密钥
3. 在`.env`文件中配置：
   ```bash
   AMAP_API_KEY=your_amap_api_key_here
   ```
4. 在`static/index.html`文件中找到以下行并替换API密钥：
   ```javascript
   script.src = 'https://webapi.amap.com/maps?v=2.0&key=YOUR_REAL_API_KEY&plugin=AMap.Scale,AMap.ToolBar,AMap.InfoWindow';
   ```

**注意：** 
- 项目默认使用演示密钥，实际部署前必须替换为真实密钥
- 高德地图API密钥需要配置域名白名单才能正常使用
- 建议为开发和生产环境分别申请不同的API密钥

### 4. 启动应用

```bash
# 开发模式启动
python main.py

# 或使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 访问应用

打开浏览器访问：`http://localhost:8000`

## 📁 项目结构

```
火车沿途风景/
├── main.py              # FastAPI主应用
├── requirements.txt     # Python依赖
├── env.example          # 环境变量示例
├── README.md           # 项目说明
└── static/
    └── index.html      # 前端页面
```

## 🎮 使用说明

### 1. 搜索车次
- 在首页输入起点、终点和出发日期
- 点击"搜索车次"按钮
- 系统将调用AI模型返回可选车次

### 2. 选择车次
- 浏览推荐的车次列表
- 查看车次信息（发车时间、到达时间、票价等）
- 点击选择心仪的车次

### 3. 探索沿途
- 系统自动获取选定车次的沿途站点信息
- 查看每个站点的主要景点和特色美食
- 享受丰富的图文介绍和视觉体验

## 🔧 API接口

### 搜索车次
```http
POST /api/search-trains
Content-Type: application/json

{
  "origin": "北京",
  "destination": "上海", 
  "departure_date": "2024-01-15"
}
```

### 获取路线信息
```http
POST /api/get-route-info
Content-Type: application/json

{
  "train_number": "G1033",
  "origin": "北京",
  "destination": "上海"
}
```

## 🎨 设计特色

### Bento Grid布局
- 采用现代化的网格布局系统
- 灵活的响应式设计
- 优雅的卡片组织方式

### Apple风格动效
- 流畅的滚动触发动画
- 悬停状态的微交互
- 渐进式加载效果

### 视觉系统
- 高质量在线图片资源
- 统一的图标语言
- 科技感的渐变配色

## 🔮 开发计划

- [ ] 集成真实12306API
- [ ] 增加用户登录系统
- [ ] 添加收藏功能
- [ ] 实现离线地图
- [ ] 支持多语言
- [ ] 移动端App

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Tailwind CSS](https://tailwindcss.com/) - 优秀的CSS框架
- [Font Awesome](https://fontawesome.com/) - 丰富的图标库
- [Unsplash](https://unsplash.com/) - 高质量免费图片
- [阿里百炼](https://dashscope.aliyun.com/) - 强大的AI能力

---

**火车沿途风景** - 让每一次旅行都成为发现之旅 🎌 

## 🗺️ 地图功能

### 功能特性
- **站点标注**：在地图上显示火车沿途所有站点
- **路线绘制**：用蓝色折线连接所有途径站点
- **信息窗口**：点击站点查看详细信息
  - 站序和站名
  - 到达/发车时间
  - 停车时长
  - 周边景点和美食推荐
- **交互体验**：
  - 鼠标悬浮显示站序
  - 点击站点居中显示
  - 暗色主题适配整体设计

### 地图样式
- 使用高德地图暗色主题
- 自定义站点标记样式
- 主要站点使用橙色标记
- 普通站点使用蓝色标记
- 响应式设计，适配移动端

## 📱 使用指南 