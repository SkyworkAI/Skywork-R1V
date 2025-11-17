#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一的批量测试结果可视化工具

支持在Web界面输入jsonl路径并查看测试结果

用法:
    python3 visual_unified.py [port]
"""

import json
import os
import sys
import re
import base64
from io import BytesIO
from PIL import Image
import webbrowser
import threading
import time
from flask import Flask, render_template_string, jsonify, send_file, request

app = Flask(__name__)

# 全局变量存储结果数据
RESULTS_DATA = []
CURRENT_FILE = ""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>统一测试结果可视化</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .file-input-section {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .file-input-group {
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .file-input-group input {
            flex: 1;
            min-width: 300px;
            padding: 12px 20px;
            border: 2px solid white;
            border-radius: 8px;
            font-size: 1em;
            background: white;
        }
        
        .file-input-group button {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            background: white;
            color: #667eea;
            transition: all 0.3s;
        }
        
        .file-input-group button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .file-input-group button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .current-file {
            margin-top: 10px;
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        .stats {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }
        
        .stat-item {
            padding: 10px 20px;
        }
        
        .stat-item strong {
            font-size: 1.5em;
        }
        
        .content {
            padding: 30px;
            max-height: 65vh;
            overflow-y: auto;
        }
        
        .test-case {
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            margin-bottom: 25px;
            background: #f9f9f9;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .test-case:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .test-case.success {
            border-left: 5px solid #28a745;
        }
        
        .test-case.error {
            border-left: 5px solid #dc3545;
        }
        
        .case-title {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px 20px;
            font-weight: bold;
            font-size: 1.1em;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .case-title .badge {
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .case-content {
            padding: 20px;
        }
        
        .section {
            margin-bottom: 20px;
        }
        
        .section-title {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.1em;
            display: flex;
            align-items: center;
        }
        
        .section-title::before {
            content: '▸';
            margin-right: 8px;
            font-size: 1.3em;
        }
        
        .question-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            border-radius: 5px;
            font-size: 1.05em;
        }
        
        .answer-box {
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            border-radius: 5px;
            white-space: pre-wrap;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .error-box {
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 15px;
            border-radius: 5px;
            color: #721c24;
        }
        
        .image-section {
            text-align: center;
            margin: 15px 0;
        }
        
        .image-section img {
            max-width: 250px;
            max-height: 250px;
            border-radius: 8px;
            border: 2px solid #667eea;
            cursor: pointer;
            transition: transform 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .image-section img:hover {
            transform: scale(1.05);
        }
        
        .image-path {
            margin-top: 10px;
            font-size: 0.85em;
            color: #666;
            word-break: break-all;
        }
        
        .generated-images {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 200px));
            gap: 15px;
            margin-top: 10px;
        }
        
        .generated-images img {
            width: 100%;
            max-height: 150px;
            object-fit: contain;
            border-radius: 8px;
            border: 2px solid #667eea;
            cursor: pointer;
            background: white;
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            padding-top: 50px;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
        }
        
        .modal-content {
            margin: auto;
            display: block;
            width: 80%;
            max-width: 900px;
            max-height: 85%;
            object-fit: contain;
        }
        
        .close {
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
        }
        
        .close:hover {
            color: #bbb;
        }
        
        .message {
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }
        
        .message.info {
            background: #d1ecf1;
            border-left: 4px solid #0c5460;
            color: #0c5460;
        }
        
        .message.error {
            background: #f8d7da;
            border-left: 4px solid #721c24;
            color: #721c24;
        }
        
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 5px;
        }
        
        @media (max-width: 768px) {
            .container {
                border-radius: 0;
            }
            
            h1 {
                font-size: 1.8em;
            }
            
            .stats {
                flex-direction: column;
            }
            
            .file-input-group {
                flex-direction: column;
            }
            
            .file-input-group input {
                min-width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 统一测试结果可视化</h1>
            <div class="file-input-section">
                <div class="file-input-group">
                    <input type="text" id="filePathInput" placeholder="输入JSONL文件路径 (例如: ./result_deepresearch.jsonl)" />
                    <button id="loadButton" onclick="loadFile()">加载文件</button>
                </div>
                <div class="current-file" id="currentFile">
                    当前文件: <span id="currentFileName">未加载</span>
                </div>
            </div>
            <div class="stats">
                <div class="stat-item">
                    <div>总测试数</div>
                    <strong id="totalCount">0</strong>
                </div>
                <div class="stat-item">
                    <div>✅ 成功</div>
                    <strong id="successCount">0</strong>
                </div>
                <div class="stat-item">
                    <div>❌ 失败</div>
                    <strong id="errorCount">0</strong>
                </div>
            </div>
        </div>
        
        <div class="content" id="content">
            <div class="message info">
                💡 请在上方输入JSONL文件路径并点击"加载文件"按钮
            </div>
        </div>
    </div>

    <div id="imageModal" class="modal">
        <span class="close" onclick="closeModal()">&times;</span>
        <img class="modal-content" id="modalImage">
    </div>

    <script>
        let currentResults = [];
        
        async function loadFile() {
            const filePath = document.getElementById('filePathInput').value.trim();
            const loadButton = document.getElementById('loadButton');
            const content = document.getElementById('content');
            
            if (!filePath) {
                content.innerHTML = '<div class="message error">❌ 请输入文件路径</div>';
                return;
            }
            
            loadButton.disabled = true;
            loadButton.textContent = '加载中...';
            content.innerHTML = '<div class="message info">⏳ 正在加载文件...</div>';
            
            try {
                const response = await fetch('/api/load', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ file_path: filePath })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('currentFileName').textContent = filePath;
                    await loadData();
                } else {
                    content.innerHTML = `<div class="message error">❌ 加载失败: ${result.error}</div>`;
                }
            } catch (error) {
                content.innerHTML = `<div class="message error">❌ 加载失败: ${error.message}</div>`;
            } finally {
                loadButton.disabled = false;
                loadButton.textContent = '加载文件';
            }
        }
        
        async function loadData() {
            try {
                const response = await fetch('/api/results');
                const data = await response.json();
                
                if (data.length === 0) {
                    document.getElementById('content').innerHTML = 
                        '<div class="message info">📭 文件中没有数据</div>';
                    return;
                }
                
                currentResults = data;
                renderResults(data);
            } catch (error) {
                console.error('加载数据失败:', error);
                document.getElementById('content').innerHTML = 
                    '<div class="message error">❌ 加载失败: ' + error.message + '</div>';
            }
        }
        
        function renderResults(results) {
            // 更新统计
            const total = results.length;
            const success = results.filter(r => !r.response.error).length;
            const error = total - success;
            
            document.getElementById('totalCount').textContent = total;
            document.getElementById('successCount').textContent = success;
            document.getElementById('errorCount').textContent = error;
            
            // 渲染测试用例
            const content = document.getElementById('content');
            
            let html = '';
            results.forEach((result, idx) => {
                const hasError = result.response.error;
                const statusClass = hasError ? 'error' : 'success';
                const statusBadge = hasError ? '❌ 失败' : '✅ 成功';
                
                html += `<div class="test-case ${statusClass}">
                    <div class="case-title">
                        <span>🧪 测试 #${idx + 1}</span>
                        <span class="badge">${statusBadge}</span>
                    </div>
                    <div class="case-content">`;
                
                // 图片
                if (result.image && result.image.trim()) {
                    const imgUrl = '/api/input_image?idx=' + idx;
                    const imgName = result.image.split('/').pop();
                    html += `<div class="section">
                        <div class="section-title">🖼️ 输入图片</div>
                        <div class="image-section">
                            <img src="${imgUrl}" alt="输入图片" onclick="showModal('${imgUrl}')" onerror="this.style.display='none'">
                            <div class="image-path">${escapeHtml(result.image)}</div>
                        </div>
                    </div>`;
                }
                
                // 问题
                html += `<div class="section">
                    <div class="section-title">❓ 问题</div>
                    <div class="question-box">${escapeHtml(result.question)}</div>
                </div>`;
                
                // 响应
                if (hasError) {
                    html += `<div class="section">
                        <div class="section-title">❌ 错误</div>
                        <div class="error-box">${escapeHtml(result.response.error)}</div>
                    </div>`;
                } else {
                    const fullResponse = result.response.full_response || '';
                    html += `<div class="section">
                        <div class="section-title">✅ 回答</div>
                        <div class="answer-box">${escapeHtml(fullResponse)}</div>
                    </div>`;
                    
                    // 生成的图片
                    if (result.generated_image_count > 0) {
                        html += `<div class="section">
                            <div class="section-title">🖼️ 生成的图片 (${result.generated_image_count})</div>
                            <div class="generated-images">`;
                        
                        for (let i = 0; i < result.generated_image_count; i++) {
                            const genImgUrl = `/api/generated_image?idx=${idx}&img_idx=${i}`;
                            html += `<img src="${genImgUrl}" alt="生成图片 ${i+1}" onclick="showModal('${genImgUrl}')">`;
                        }
                        
                        html += `</div></div>`;
                    }
                }
                
                html += `</div></div>`;
            });
            
            content.innerHTML = html;
        }
        
        function showModal(imageUrl) {
            document.getElementById('imageModal').style.display = 'block';
            document.getElementById('modalImage').src = imageUrl;
        }
        
        function closeModal() {
            document.getElementById('imageModal').style.display = 'none';
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        window.onclick = function(event) {
            const modal = document.getElementById('imageModal');
            if (event.target === modal) {
                closeModal();
            }
        }
        
        // 支持回车键加载文件
        document.getElementById('filePathInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                loadFile();
            }
        });
    </script>
</body>
</html>
"""


def extract_images_from_response(response_data):
    """从响应中提取生成的图片"""
    images = []

    if "full_response" in response_data:
        content = response_data["full_response"]
        # 提取base64图片
        image_matches = re.findall(
            r'data:image/[^;]+;base64,([A-Za-z0-9+/=\s]+?)(?=["\\},]|$)',
            content,
            re.DOTALL,
        )

        for img_data in image_matches:
            try:
                img_data_clean = re.sub(r"\s", "", img_data)
                img_bytes = base64.b64decode(img_data_clean)
                img = Image.open(BytesIO(img_bytes))
                images.append(img)
            except Exception as e:
                print(f"解码图片失败: {e}")

    return images


def load_results(results_jsonl):
    """加载结果文件"""
    results = []

    if not os.path.exists(results_jsonl):
        raise FileNotFoundError(f"文件不存在: {results_jsonl}")

    with open(results_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    result = json.loads(line)
                    # 提取生成的图片
                    generated_images = extract_images_from_response(result["response"])
                    result["generated_images"] = generated_images
                    results.append(result)
                except Exception as e:
                    print(f"解析行失败: {e}, 行内容: {line[:100]}")

    return results


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/load", methods=["POST"])
def load_file():
    """加载新的结果文件"""
    global RESULTS_DATA, CURRENT_FILE

    try:
        data = request.get_json()
        file_path = data.get("file_path", "").strip()

        if not file_path:
            return jsonify({"success": False, "error": "文件路径为空"})

        # 尝试加载文件
        results = load_results(file_path)
        RESULTS_DATA = results
        CURRENT_FILE = file_path

        return jsonify(
            {
                "success": True,
                "count": len(results),
                "file": file_path,
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/results")
def get_results():
    """返回结果数据"""
    data = []

    for result in RESULTS_DATA:
        data.append(
            {
                "image": result.get("image", ""),
                "question": result.get("question", ""),
                "response": result.get("response", {}),
                "generated_image_count": len(result.get("generated_images", [])),
            }
        )

    return jsonify(data)


@app.route("/api/input_image")
def serve_input_image():
    """返回输入图片"""
    try:
        idx = int(request.args.get("idx", 0))
        result = RESULTS_DATA[idx]
        image_path = result.get("image", "")

        if image_path and image_path.strip() and os.path.exists(image_path):
            return send_file(image_path)
        else:
            raise ValueError("图片不存在")
    except Exception as e:
        # 返回占位图
        img = Image.new("RGB", (300, 200), color="#f0f0f0")
        img_io = BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png")


@app.route("/api/generated_image")
def serve_generated_image():
    """返回生成的图片"""
    try:
        idx = int(request.args.get("idx", 0))
        img_idx = int(request.args.get("img_idx", 0))

        result = RESULTS_DATA[idx]
        images = result.get("generated_images", [])

        if img_idx < len(images):
            img = images[img_idx]
            img_io = BytesIO()
            img.save(img_io, "PNG")
            img_io.seek(0)
            return send_file(img_io, mimetype="image/png")
        else:
            raise ValueError("图片索引超出范围")
    except Exception as e:
        # 返回占位图
        img = Image.new("RGB", (300, 200), color="#f0f0f0")
        img_io = BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png")


def open_browser(port):
    """延迟打开浏览器"""
    time.sleep(1.5)
    webbrowser.open(f"http://localhost:{port}")


def main():
    port = 22895  # 默认端口

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            print(f"⚠️  端口参数无效，使用默认端口: {port}")

    print(f"🚀 启动统一可视化服务器...")
    print(f"🌐 访问地址: http://localhost:{port}")
    print(f"💡 提示: 在网页中输入JSONL文件路径来加载数据")
    print(f"💡 提示: 按 Ctrl+C 停止服务器\n")

    # 在新线程中打开浏览器
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()

    # 启动Flask应用
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()

