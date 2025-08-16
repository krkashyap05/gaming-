from flask import Flask, request, jsonify, render_template, send_file
import yt_dlp
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info.get('formats', []):
                if f.get('ext') in ['mp4', 'webm'] and f.get('vcodec') != 'none':
                    formats.append({
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'resolution': f.get('resolution'),
                        'filesize': f.get('filesize'),
                        'vcodec': f.get('vcodec'),
                        'acodec': f.get('acodec'),
                    })

            audio_formats = []
            for f in info.get('formats', []):
                 if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    audio_formats.append({
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'filesize': f.get('filesize'),
                        'acodec': f.get('acodec'),
                        'abr': f.get('abr')
                    })


            video_info = {
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'formats': formats,
                'audio_formats': audio_formats
            }
            return jsonify(video_info)
        except yt_dlp.utils.DownloadError as e:
            return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    format_id = request.args.get('format_id')
    title = request.args.get('title', 'video') # Use a default title if not provided
    ext = request.args.get('ext', 'mp4') # Use a default extension if not provided


    if not url or not format_id:
        return "Missing URL or format_id", 400

    # Sanitize title to prevent directory traversal
    safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()

    download_path = os.path.join('downloads', f'{safe_title}.{ext}')

    # Ensure a downloads directory exists
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    ydl_opts = {
        'format': format_id,
        'outtmpl': download_path,
        'quiet': True,
        'no_warnings': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            return send_file(download_path, as_attachment=True)
        except Exception as e:
            return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
