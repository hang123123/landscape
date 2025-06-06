#!/usr/bin/env python3
"""
火车沿途风景 - 启动脚本
"""
import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """检查依赖是否已安装"""
    try:
        import fastapi
        import uvicorn
        import httpx
        import pydantic
        import jinja2
        import aiofiles
        import dotenv
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_env_file():
    """检查环境变量文件"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("⚠️  未找到 .env 文件")
            print("💡 提示: 请复制 env.example 为 .env 并配置您的API密钥")
            print("   cp env.example .env")
            print("   然后编辑 .env 文件填入您的阿里百炼API密钥")
        else:
            print("⚠️  未找到环境变量文件")
        return False
    
    print("✅ 环境变量文件存在")
    return True

def check_static_files():
    """检查静态文件目录"""
    static_dir = Path("static")
    index_file = static_dir / "index.html"
    
    if not static_dir.exists():
        print("❌ 静态文件目录不存在")
        return False
    
    if not index_file.exists():
        print("❌ 主页文件不存在")
        return False
    
    print("✅ 静态文件检查通过")
    return True

def main():
    """主函数"""
    print("🚄 火车沿途风景 - 系统检查")
    print("=" * 50)
    
    # 检查依赖
    if not check_requirements():
        sys.exit(1)
    
    # 检查环境变量
    env_ok = check_env_file()
    
    # 检查静态文件
    if not check_static_files():
        sys.exit(1)
    
    if env_ok:
        print("✅ 系统检查通过")
    else:
        print("⚠️  系统检查完成（将使用模拟数据）")
    
    print("=" * 50)
    print("🚀 启动服务...")
    
    # 启动应用
    try:
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 