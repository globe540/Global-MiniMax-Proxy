from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 從環境變數讀取 OpenRouter API key
OPENROUTER_KEY = os.environ.get('OPENROUTER_KEY')

@app.route('/v1/chat/completions', methods=['POST'])
def proxy():
    try:
        # 檢查 key 是否存在
        if not OPENROUTER_KEY:
            return jsonify({
                "error": "OPENROUTER_KEY not found in environment variables. Please set it in Vercel Settings."
            }), 500

        # 取得客戶傳來的資料
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        # 強制使用 MiniMax M2.5（使用 OpenRouter 目前正確的 model ID）
        data['model'] = 'minimax/minimax-m2.5'

        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        }

        # 轉發請求到 OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60  # 設定 60 秒 timeout，避免卡死
        )

        # 回傳 OpenRouter 的結果
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        # 捕捉網路請求相關錯誤
        return jsonify({
            "error": f"Request to OpenRouter failed: {str(e)}"
        }), 502

    except Exception as e:
        # 其他意外錯誤
        return jsonify({
            "error": f"Proxy server error: {str(e)}"
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
