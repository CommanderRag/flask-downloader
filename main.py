import os, re, time, threading
from flask import Flask, request, render_template, send_from_directory
import youtube_dl

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "downloaded"

keepcharacters = (' ', '.', '_', '&', '-', '!', '#', '(', ')')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():

    ydl_info = youtube_dl.YoutubeDL({'format', 'best'})

    r = request.get_json(force=True)
    url = r['url']
    
    info = ydl_info.extract_info(url=url, download=False)

    filename = info.get('title') + '.' + info.get('ext')

    ydl = youtube_dl.YoutubeDL({'outtmpl': 'downloaded/' + filename, 'format': 'best'})

    try:
        result = ydl.extract_info(url=url, download=True)
    except Exception as e:
        print(e)
        return "400"

    return send_from_directory('downloaded', filename, as_attachment=True), schedule_delete(filename)

    
@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', as_attachment=True)

def schedule_delete(f):
    time.sleep(6)
    os.remove(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], f))


if __name__ == '__main__':
    app.run()