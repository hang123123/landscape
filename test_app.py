#!/usr/bin/env python3
"""
火车沿途风景 - 功能测试脚本
"""

def test_project_structure():
    """测试项目结构完整性"""
    import os
    from pathlib import Path
    
    print("🔍 检查项目结构...")
    
    required_files = [
        "main.py",
        "ai_client.py", 
        "requirements.txt",
        "README.md",
        "env.example",
        "start.py",
        "static/index.html"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_files:
        print(f"  ❌ 缺少文件: {missing_files}")
        return False
    
    print("✅ 项目结构完整")
    return True

def test_dependencies():
    """测试依赖导入"""
    print("\n📦 检查依赖...")
    
    try:
        import fastapi
        print("  ✅ FastAPI")
        
        import uvicorn
        print("  ✅ Uvicorn")
        
        import httpx
        print("  ✅ HTTPX")
        
        import pydantic
        print("  ✅ Pydantic")
        
        from dotenv import load_dotenv
        print("  ✅ Python-dotenv")
        
        print("✅ 所有依赖正常")
        return True
        
    except ImportError as e:
        print(f"  ❌ 依赖导入失败: {e}")
        return False

def test_ai_client():
    """测试AI客户端"""
    print("\n🤖 检查AI客户端...")
    
    try:
        from ai_client import AlibabaAIClient
        client = AlibabaAIClient()
        print("  ✅ AI客户端创建成功")
        
        # 测试模拟数据
        mock_trains = client._get_mock_trains()
        if len(mock_trains) > 0:
            print(f"  ✅ 模拟车次数据 ({len(mock_trains)}条)")
        
        mock_route = client._get_mock_route()
        if "stations" in mock_route:
            print(f"  ✅ 模拟路线数据 ({len(mock_route['stations'])}个站点)")
        
        print("✅ AI客户端功能正常")
        return True
        
    except Exception as e:
        print(f"  ❌ AI客户端测试失败: {e}")
        return False

def test_fastapi_app():
    """测试FastAPI应用"""
    print("\n🚀 检查FastAPI应用...")
    
    try:
        from main import app
        print("  ✅ FastAPI应用导入成功")
        
        # 检查路由
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/api/search-trains", "/api/get-route-info", "/api/health"]
        
        for route in expected_routes:
            if route in routes:
                print(f"  ✅ 路由: {route}")
            else:
                print(f"  ❌ 缺少路由: {route}")
                return False
        
        print("✅ FastAPI应用配置正确")
        return True
        
    except Exception as e:
        print(f"  ❌ FastAPI应用测试失败: {e}")
        return False

def test_html_structure():
    """测试HTML结构"""
    print("\n🌐 检查前端页面...")
    
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # 检查关键元素
        checks = [
            ("Tailwind CSS", "tailwindcss.com" in html_content),
            ("Font Awesome", "font-awesome" in html_content or "fontawesome" in html_content),
            ("搜索表单", "searchForm" in html_content),
            ("车次选择", "trainSection" in html_content),
            ("路线信息", "routeSection" in html_content),
            ("动画效果", "fade-in" in html_content or "slide-up" in html_content),
            ("响应式设计", "md:grid-cols" in html_content),
        ]
        
        all_passed = True
        for check_name, condition in checks:
            if condition:
                print(f"  ✅ {check_name}")
            else:
                print(f"  ❌ {check_name}")
                all_passed = False
        
        if all_passed:
            print("✅ 前端页面结构完整")
            return True
        else:
            return False
        
    except Exception as e:
        print(f"  ❌ HTML检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚄 火车沿途风景 - 项目完整性检查")
    print("=" * 60)
    
    tests = [
        test_project_structure,
        test_dependencies,
        test_ai_client,
        test_fastapi_app,
        test_html_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print("")
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 项目完整性检查通过！")
        print("\n🚀 启动建议:")
        print("1. 复制环境变量文件: cp env.example .env")
        print("2. 配置阿里百炼API密钥（可选，不配置将使用模拟数据）")
        print("3. 安装依赖: pip install -r requirements.txt")
        print("4. 启动应用: python start.py")
        print("5. 访问: http://localhost:8000")
        return True
    else:
        print("❌ 项目存在问题，请检查上述错误")
        return False

if __name__ == "__main__":
    main() 