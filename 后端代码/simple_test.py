print("Testing basic imports...")
try:
    from flask import Flask
    print("✓ Flask imported successfully")
except Exception as e:
    print(f"✗ Flask import failed: {e}")

try:
    from flask_cors import CORS
    print("✓ Flask-CORS imported successfully")
except Exception as e:
    print(f"✗ Flask-CORS import failed: {e}")

try:
    from transformers import BertTokenizer
    print("✓ Transformers imported successfully")
except Exception as e:
    print(f"✗ Transformers import failed: {e}")

print("\nTesting BERT model path...")
import os
bert_path = "../BERT模型/BERT"
if os.path.exists(bert_path):
    print(f"✓ BERT path exists: {bert_path}")
    files = os.listdir(bert_path)
    print(f"  Files: {files}")
else:
    print(f"✗ BERT path not found: {bert_path}")