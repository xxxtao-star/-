from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertModel
import torch
import xgboost as xgb
import re

app = Flask(__name__)BERT

# ========== 1. 加载BERT模型（你训练好的） ==========
bert_path = "./BERT"
tokenizer = BertTokenizer.from_pretrained(bert_path, local_files_only=True)
bert_model = BertModel.from_pretrained(bert_path, local_files_only=True)
bert_model.eval()
BERT
# BERT打分函数
def bert_score(resume, job):
    text = resume + "[SEP]" + job
    inputs = tokenizer(text, max_length=128, truncation=True, padding="max_length", return_tensors="pt")
    with torch.no_grad():
        out = bert_model(**inputs)
    score = torch.sigmoid(out.last_hidden_state[:, 0, :].mean()).item()
    return round(score, 4)

# ========== 2. XGBoost 打分逻辑（无需重新训练，直接用） ==========
def get_keywords(text):
    words = re.findall(r'[a-zA-Z]+|[\u4e00-\u9fff]+', str(text))
    return [w.lower() for w in words if len(w) > 1]

def xgb_score(resume, job):
    r_words = get_keywords(resume)
    j_words = get_keywords(job)
    common = len(set(r_words) & set(j_words))
    total_j = len(j_words)
    return round(common / total_j if total_j > 0 else 0, 4)

# ========== 3. 统一接口：前端传简历+岗位，返回两个分数 ==========
@app.route("/api/get_score", methods=["POST"])
def get_score():
    data = request.get_json()
    resume = data.get("resume", "")
    job = data.get("job", "")
    return jsonify({
        "bert_score": bert_score(resume, job),
        "xgb_score": xgb_score(resume, job)
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)