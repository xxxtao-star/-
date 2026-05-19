import sys
import os

print("=" * 50)
print("启动诊断脚本")
print("=" * 50)

# 测试基本导入
print("\n[1] 测试Python环境...")
print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")

# 测试Flask导入
print("\n[2] 测试Flask导入...")
try:
    from flask import Flask, request, jsonify
    print("✓ Flask导入成功")
except Exception as e:
    print(f"✗ Flask导入失败: {e}")
    sys.exit(1)

# 测试CORS导入
print("\n[3] 测试Flask-CORS导入...")
try:
    from flask_cors import CORS
    print("✓ Flask-CORS导入成功")
except Exception as e:
    print(f"✗ Flask-CORS导入失败: {e}")
    sys.exit(1)

# 测试Transformers导入
print("\n[4] 测试Transformers导入...")
try:
    from transformers import BertTokenizer, BertModel
    print("✓ Transformers导入成功")
except Exception as e:
    print(f"✗ Transformers导入失败: {e}")
    sys.exit(1)

# 测试BERT模型路径
print("\n[5] 测试BERT模型路径...")
bert_path = "../BERT模型/BERT"
full_path = os.path.abspath(bert_path)
print(f"BERT相对路径: {bert_path}")
print(f"BERT绝对路径: {full_path}")
print(f"路径存在: {os.path.exists(full_path)}")

if os.path.exists(full_path):
    files = os.listdir(full_path)
    print(f"BERT目录文件: {files}")

# 测试模型加载
print("\n[6] 测试BERT模型加载...")
try:
    tokenizer = BertTokenizer.from_pretrained(full_path, local_files_only=True)
    print("✓ Tokenizer加载成功")
    bert_model = BertModel.from_pretrained(full_path, local_files_only=True)
    print("✓ Model加载成功")
except Exception as e:
    print(f"✗ 模型加载失败: {e}")
    sys.exit(1)

print("\n[7] 诊断完成! 所有测试通过!")