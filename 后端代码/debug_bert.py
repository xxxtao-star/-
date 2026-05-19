import os
import sys

print("Current working directory:", os.getcwd())
print("Python executable:", sys.executable)
print("Python version:", sys.version)

bert_path = "../BERT模型/BERT"
full_path = os.path.abspath(bert_path)
print("\nBERT path:", bert_path)
print("Full path:", full_path)
print("Path exists:", os.path.exists(full_path))

if os.path.exists(full_path):
    print("Files in BERT directory:", os.listdir(full_path))

try:
    print("\nTrying to import transformers...")
    from transformers import BertTokenizer, BertModel
    print("✓ Transformers imported")

    print("\nTrying to load BERT model...")
    tokenizer = BertTokenizer.from_pretrained(full_path, local_files_only=True)
    print("✓ Tokenizer loaded")

    bert_model = BertModel.from_pretrained(full_path, local_files_only=True)
    print("✓ Model loaded")
    print("BERT model loaded successfully!")
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()