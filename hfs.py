from flask import Flask, request, send_file
import os
from PIL import Image
import threading
import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

def run_flask():
    webbrowser.open_new('http://localhost:5000/')
    app.run()
    

@app.route('/')
def index():
    return '''
        <html>
          <head>
            <meta charset="utf-8">
            <title>文件分享</title>
          </head>
          <body>
            <div id="drop_zone" style="border: 2px dashed gray; padding: 10px; width: 400px; height: 300px;">
              請將文件拖曳到此處上傳!
            </div>
            <div id="result" style="margin-top: 10px;"></div>

            <script>
              function handleDrop(event) {
                event.preventDefault();

                // 抓取上傳的文件
                var file = event.dataTransfer.files[0];

                // 創建FormData對象
                var formData = new FormData();
                formData.append('file', file);

                // 發送上傳請求
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/upload');
                xhr.onload = function() {
                  if (xhr.status === 200) {
                    var url = JSON.parse(xhr.responseText).url;
                    document.getElementById('result').innerHTML = '下載連結：<a href="' + url + '">' + url + '</a>';
                  } else {
                    document.getElementById('result').innerHTML = '上傳失敗';
                  }
                };
                xhr.send(formData);
              }

              function handleDragOver(event) {
                event.preventDefault();
              }

              var dropZone = document.getElementById('drop_zone');
              dropZone.addEventListener('drop', handleDrop);
              dropZone.addEventListener('dragover', handleDragOver);
            </script>
          </body>
        </html>
    '''
def is_image(filename):
    try:
        with Image.open(filename) as im:
            return True
    except:
        return False
    
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    url = request.host_url + 'download/' + filename
    return {'url': url}

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if is_image(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        mimetype = 'image/png' if filename.endswith('.png') else 'image/jpeg'
        return send_file(path, mimetype=mimetype)
    else:
        return send_file(path, as_attachment=True)


if __name__ == '__main__':
    run_flask()
