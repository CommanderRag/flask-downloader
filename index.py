from flask import Flask, request, render_template
import youtube_dl

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(title)s.%(ext)s', 'format': 'best'})

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    r = request.get_json(force=True)
    url = r['url']
    result = ydl.extract_info(url=url, download=False)
    print("Info url:", url) 
    if(result.get('url') == None):
        return "400"
    return result['url']


if __name__ == '__main__':
    app.run()