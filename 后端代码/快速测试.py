#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""快速测试脚本 - 测试后端服务"""

import sys
import os
import subprocess
import time
import requests

print("=" * 60)
print("           简历匹配系统 - 快速测试工具")
print("=" * 60)
print()

# 步骤1: 检查Python
print("[1/5] 检查Python环境...")
try:
    print(f"  Python版本: {sys.version}")
    print("  ✓ Python检查通过")
except Exception as e:
    print(f"  ✗ Python检查失败: {e}")
    sys.exit(1)
print()

# 步骤2: 检查依赖
print("[2/5] 检查依赖包...")
required = ['flask', 'flask_cors']
optional = ['transformers', 'torch', 'pandas', 'numpy', 'scikit_learn']

all_ok = True
for pkg in required:
    try:
        __import__(pkg)
        print(f"  ✓ {pkg}")
    except ImportError:
        print(f"  ✗ {pkg} (必需)")
        all_ok = False

for pkg in optional:
    try:
        __import__(pkg)
        print(f"  ✓ {pkg} (可选)")
    except ImportError:
        print(f"  ⚠ {pkg} (可选，未安装)")

if not all_ok:
    print()
    print("⚠ 必需依赖缺失！")
    print("请运行: pip install flask flask-cors")
    print()
    print("可选依赖（用于完整功能）:")
    print("pip install transformers torch pandas numpy scikit-learn")
    print()
else:
    print("  ✓ 依赖检查完成")
print()

# 步骤3: 检查后端是否运行
print("[3/5] 检查后端服务状态...")
backend_url = "http://127.0.0.1:5000"
health_url = f"{backend_url}/api/health"

try:
    response = requests.get(health_url, timeout=2)
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ 后端服务运行正常")
        print(f"    - 状态: {data.get('status', 'unknown')}")
        print(f"    - BERT模型: {'已加载' if data.get('bert_loaded') else '未加载'}")
        backend_running = True
    else:
        print(f"  ⚠ 后端响应异常: {response.status_code}")
        backend_running = False
except requests.exceptions.ConnectionError:
    print(f"  ✗ 后端服务未运行")
    backend_running = False
except Exception as e:
    print(f"  ✗ 检查失败: {e}")
    backend_running = False
print()

# 步骤4: 如果后端未运行，尝试启动
if not backend_running:
    print("[4/5] 尝试启动后端服务...")
    print("  提示: 请手动运行 '启动后端.bat' 或 'python app.py'")
    print()
else:
    print("[4/5] 测试API接口...")
    try:
        jobs_url = f"{backend_url}/api/jobs"
        response = requests.get(jobs_url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                jobs = data.get('data', [])
                print(f"  ✓ 岗位API正常，共 {len(jobs)} 个岗位")
            else:
                print(f"  ⚠ 岗位API返回错误: {data.get('error')}")
        else:
            print(f"  ⚠ 岗位API响应异常: {response.status_code}")
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
    print()

# 步骤5: 完成
print("[5/5] 测试完成！")
print()
print("=" * 60)
print("                    总结")
print("=" * 60)

if backend_running:
    print()
    print("✅ 后端服务正常运行！")
    print("   - 后端地址: http://127.0.0.1:5000")
    print("   - 健康检查: http://127.0.0.1:5000/api/health")
    print()
    print("现在可以启动前端了：")
    print("   运行 '启动前端.bat' 或 'streamlit run app.py'")
else:
    print()
    print("❌ 后端服务未运行")
    print()
    print("请按以下步骤操作：")
    print("   1. 打开文件夹: c:\\Users\\30906\\Desktop\\作业\\简历匹配系统\\算法接口")
    print("   2. 双击运行: 启动后端.bat")
    print("   3. 等待后端启动成功")
    print("   4. 再运行此测试脚本")
print()
print("=" * 60)
print()
input("按回车键退出...")