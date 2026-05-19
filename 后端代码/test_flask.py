from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("Starting Flask test server...")
    app.run(host='127.0.0.1', port=5001, debug=True)