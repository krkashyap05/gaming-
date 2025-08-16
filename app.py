from flask import Flask, request, jsonify, render_template, send_file
import yt_dlp
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__, template_folder='.')

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    app.logger.info("Received request for /get_info")
    url = request.json.get('url')
    if not url:
        app.logger.error("URL is required in /get_info")
        return jsonify({'error': 'URL is required'}), 400

    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            # Filter for complete formats (with both video and audio)
            formats = []
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    formats.append({
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'resolution': f.get('resolution'),
                        'filesize': f.get('filesize'),
                        'vcodec': f.get('vcodec'),
                        'acodec': f.get('acodec'),
                    })

            video_info = {
                'id': info.get('id'),
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'formats': formats,
            }
            return jsonify(video_info)
        except yt_dlp.utils.DownloadError as e:
            return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['GET'])
def download():
    app.logger.info("Received request for /download")
    url = request.args.get('url')
    format_id = request.args.get('format_id')
    title = request.args.get('title', 'video') # Use a default title if not provided
    ext = request.args.get('ext', 'mp4') # Use a default extension if not provided
    video_id = request.args.get('id')


    if not url or not format_id:
        app.logger.error("Missing URL or format_id in /download")
        return "Missing URL or format_id", 400

    # Sanitize title to prevent directory traversal
    safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()

    # Create a unique filename
    if video_id:
        filename = f'{safe_title}-{video_id}.{ext}'
    else:
        # Fallback for safety, though id should always be present with the new frontend code
        import time
        filename = f'{safe_title}-{int(time.time())}.{ext}'

    download_path = os.path.join('downloads', filename)

    # Ensure a downloads directory exists
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    ydl_opts = {
        'format': format_id,
        'outtmpl': download_path,
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            app.logger.info(f"Starting ydl.download for URL: {url}")
            ydl.download([url])
            app.logger.info(f"ydl.download finished. Sending file: {download_path}")
            return send_file(download_path, as_attachment=True)
        except Exception as e:
            app.logger.error(f"An error occurred during download: {e}")
            return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
