# 🔑 阿里百炼API配置指南

## 📋 配置清单

- [ ] 阿里云账号（已实名认证）
- [ ] 开通DashScope服务
- [ ] 获取API Key
- [ ] 配置环境变量
- [ ] 验证连接

## 🚀 详细步骤

### 1. 申请阿里云账号

1. **访问阿里云官网**：https://www.aliyun.com
2. **注册账号**：点击右上角"免费注册"
3. **实名认证**：完成个人或企业实名认证（必须）

### 2. 开通DashScope服务

1. **登录控制台**：https://ecs.console.aliyun.com
2. **搜索DashScope**：在控制台搜索框输入"DashScope"
3. **访问产品页**：或直接访问 https://dashscope.console.aliyun.com/
4. **开通服务**：
   - 点击"立即开通"
   - 阅读并同意服务协议
   - 选择计费方式（推荐先试用免费额度）

### 3. 获取API Key和应用ID

1. **进入控制台**：https://dashscope.console.aliyun.com/
2. **API Key管理**：点击左侧菜单"API Key管理"
3. **创建新Key**：点击"创建新的API Key"
4. **复制保存**：妥善保存生成的API Key

**API Key格式示例**：
```
sk-26e235b4b7e54d259b936f8b76c8a062
```

5. **创建应用**：
   - 点击左侧菜单"我的应用"
   - 点击"创建应用"
   - 选择应用类型（推荐选择"Agent应用"）
   - 填写应用名称和描述
   - 配置系统提示词（可选）
   - 点击"创建"

6. **获取应用ID**：
   - 在应用列表中找到刚创建的应用
   - 点击应用名称进入详情页
   - 复制"应用ID"（app_id）

**应用ID格式示例**：
```
485f3c8e1d034a54a12a51984114b0f3
```

### 4. 配置项目

1. **复制配置文件**：
```bash
cp env.example .env
```

2. **编辑配置文件**：
```bash
# macOS/Linux
nano .env

# Windows
notepad .env
```

3. **填入API Key和应用ID**：
```bash
# 阿里百炼API配置 - 必填
ALIBABA_DASHSCOPE_API_KEY=sk-你的API密钥
ALIBABA_DASHSCOPE_APP_ID=你的应用ID

# 其他配置（可选）
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

## 🔧 技术实现说明

### API调用方式
项目使用**OpenAI兼容模式**调用阿里百炼API：

- **API端点**：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
- **模型**：`qwen-plus`（通义千问Plus）
- **认证**：Bearer Token方式
- **格式**：标准OpenAI Chat Completions格式

### 代码实现细节
```python
# ai_client.py 中的关键配置
class AlibabaAIClient:
    def __init__(self):
        self.api_key = os.getenv("ALIBABA_DASHSCOPE_API_KEY")
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        self.model = "qwen-plus"
```

## ✅ 配置验证

### 1. 启动应用测试
```bash
python start.py
```

### 2. 健康检查
```bash
curl http://localhost:8000/api/health
```

**正确配置的返回示例**：
```json
{
  "status": "healthy",
  "ai_client": "connected",
  "version": "1.0.0"
}
```

**未配置API Key的返回**：
```json
{
  "status": "healthy", 
  "ai_client": "using_mock_data",
  "version": "1.0.0"
}
```

### 3. API功能测试
```bash
curl -X POST http://localhost:8000/api/search-trains \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "北京",
    "destination": "上海", 
    "departure_date": "2024-01-15"
  }'
```

## 🚨 常见问题

### 1. API Key格式错误
- 确保API Key以 `sk-` 开头
- 检查是否包含空格或特殊字符
- 重新从控制台复制API Key

### 2. 网络连接问题
- 检查防火墙设置
- 确认可以访问 `dashscope.aliyuncs.com`
- 考虑网络代理配置

### 3. 权限和配额问题
- 确认账号已完成实名认证
- 检查DashScope服务状态
- 查看API调用配额是否充足

### 4. 环境变量问题
```bash
# 检查环境变量是否正确设置
echo $ALIBABA_DASHSCOPE_API_KEY
```

## 💡 最佳实践

1. **安全存储**：不要在代码中硬编码API Key
2. **配额管理**：设置合理的API调用限制
3. **错误处理**：实现降级到模拟数据的机制
4. **监控报警**：监控API调用状态和费用
5. **定期轮换**：定期更新API Key

## 📞 技术支持

如果遇到配置问题，可以：
1. 查看阿里云DashScope官方文档
2. 检查项目中的健康检查接口
3. 查看应用日志中的错误信息

## 💰 费用说明

### 免费额度
- 新用户通常有一定的免费调用额度
- 具体额度请查看DashScope控制台

### 计费方式
- 按调用次数计费
- 不同模型价格不同
- 建议设置消费限额

### 成本控制
1. **设置预算**：在控制台设置每日/每月消费限额
2. **监控用量**：定期查看API调用次数和费用
3. **合理使用**：开发测试期间可以使用模拟数据

## 🔧 故障排除

### 问题1：API Key无效
**症状**：调用失败，返回401错误
**解决**：
- 检查API Key是否正确复制
- 确认API Key没有过期
- 验证DashScope服务已开通

### 问题2：服务未开通
**症状**：返回"服务未开通"错误
**解决**：
- 确认已在控制台开通DashScope
- 检查阿里云账号实名认证状态

### 问题3：余额不足
**症状**：调用失败，提示余额不足
**解决**：
- 充值阿里云账户余额
- 或使用模拟数据模式继续开发

### 问题4：调用限流
**症状**：频繁调用失败
**解决**：
- 增加调用间隔
- 升级到更高级别的服务

## 🔒 安全建议

1. **保护API Key**：
   - 不要提交到代码仓库
   - 不要在公开场所分享
   - 定期更换API Key

2. **访问控制**：
   - 设置IP白名单（如果支持）
   - 监控异常调用

3. **环境隔离**：
   - 开发/测试/生产使用不同API Key
   - 分别设置不同的预算限制

---

配置完成后，您的应用就可以使用真正的AI大模型来生成景点和美食推荐了！🎉 