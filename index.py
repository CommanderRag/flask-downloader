import os, re, time, threading
from flask import Flask, request, render_template, send_from_directory
import youtube_dl

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "downloaded"

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():

    ydl = youtube_dl.YoutubeDL({'outtmpl': 'downloaded/%(title)s.%(ext)s', 'format': 'best', 'source-address': request.remote_addr, 'referer': 'youtube.com'})

    r = request.get_json(force=True)
    url = r['url']
    result = ydl.extract_info(url=url, download=True)
    
    title = result.get('title')

    print("Info url:", url) 
    # print(result)

    for f in os.listdir(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])):
        if(re.match(title, f)):
            thread = threading.Thread(target=schedule_delete, args=[f])
            thread.start()
            return send_from_directory(app.config['UPLOAD_FOLDER'], f, as_attachment=True)


    return "400"
    
def schedule_delete(f):
    time.sleep(6)
    os.remove(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], f))

if __name__ == '__main__':
    app.run()