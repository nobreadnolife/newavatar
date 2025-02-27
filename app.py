import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process_image():
    """接收图片，去除背景后返回 PNG"""
    if 'image' not in request.files:
        return {"error": "没有上传图片"}, 400

    file = request.files['image']
    image_bytes = file.read()

    # 处理抠图
    image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    output = remove(image)  # 只抠图，不合成背景

    # 返回处理后的透明 PNG
    img_io = io.BytesIO()
    output.save(img_io, format="PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")
