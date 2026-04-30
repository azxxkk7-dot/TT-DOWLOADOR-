import os
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def tiktok_api():
    payload = request.get_json()
    url = payload.get('url')

    if not url:
        return jsonify({"status": "error", "message": "Null Input"}), 400

    try:
        api_url = "https://www.tikwm.com/api/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        data = {'url': url, 'hd': 1}
        
        response = requests.post(api_url, data=data, headers=headers).json()

        if response.get('code') == 0:
            res_data = response['data']
            images = res_data.get('images')
            audio_url = res_data.get('music')
            
            result = {
                "status": "success",
                "audio": audio_url,
                "type": "video"
            }

            if images:
                result["type"] = "photo"
                result["images"] = images
            else:
                result["sd"] = res_data.get('play')
                result["hd"] = res_data.get('hdplay') or res_data.get('play')

            return jsonify(result)
        else:
            return jsonify({"status": "error", "message": response.get('msg', 'API REJECTED')}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Handler untuk Vercel
def handler(event, context):
    return app(event, context)
