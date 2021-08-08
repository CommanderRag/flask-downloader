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

    ydl = youtube_dl.YoutubeDL({'outtmpl': 'downloaded/%(title)s.%(ext)s', 'format': 'best'})

    r = request.get_json(force=True)
    url = r['url']
    try:
        result = ydl.extract_info(url=url, download=True)
    except Exception as e:
        print(e)
        return "400"

    
    title = result.get('title')

    print("Info url:", url) 


    for f in os.listdir(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])):
        if(re.match(title, f)):
            thread = threading.Thread(target=schedule_delete, args=[f])
            thread.start()
            return send_from_directory('downloaded', f, as_attachment=True)
            # return send_from_directory(directory=os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), filename=f, as_attachment=True)


    return "400"
    
@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', as_attachment=True)

def schedule_delete(f):
    time.sleep(6)
    os.remove(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], f))


if __name__ == '__main__':
    app.run()