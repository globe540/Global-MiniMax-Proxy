from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 從環境變數讀取你的 OpenRouter API key（安全）
OPENROUTER_KEY = os.environ.get('OPENROUTER_KEY')

@app.route('/v1/chat/completions', methods=['POST'])
def proxy():
    if not OPENROUTER_KEY:
        return jsonify({"error": "API key not set"}), 500

    data = request.json
    # 強制使用 MiniMax M2.5（你可以之後改成讓客戶指定）
    data['model'] = 'minimax/m2.5'

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY",
        "Content-Type": "application/json"
    }

    # 轉發到 OpenRouter
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    # 回傳結果給客戶
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run()