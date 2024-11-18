import os
from urllib.parse import urlparse
from flask import Flask, request, render_template, send_from_directory
from spleeter.separator import Separator
from yt_dlp import YoutubeDL  # Moved to the top

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """
    Renders the home page with a form to input a YouTube URL.
    """
    return render_template('index.html')
@app.route('/process', methods=['POST'])

def process():
    """
    Processes the provided YouTube URL, downloads the MP3, separates tracks,
    and provides download links for the output files.
    """
    try:
        youtube_url = request.form['url']
        if not youtube_url:
            return "No URL provided", 400

        # Validate the YouTube URL
        parsed_url = urlparse(youtube_url)
        if not parsed_url.netloc.endswith('youtube.com') and not parsed_url.netloc.endswith('youtu.be'):
            return "Invalid YouTube URL", 400

        # Download audio using yt-dlp
        from yt_dlp import YoutubeDL
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(UPLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            title = info['title']
            mp3_path = os.path.join(UPLOAD_FOLDER, f"{title}.mp3")

        # Run Spleeter 5-stem separation
        separator = Separator("spleeter:5stems")
        output_path = os.path.join(PROCESSED_FOLDER)
        os.makedirs(output_path, exist_ok=True)
        separator.separate_to_file(mp3_path, output_path)

        # Generate download links
        download_links = {
            "original_mp3": f"/download/uploads/{title}.mp3",
            "vocals": f"/download/processed/{title}/vocals.wav",
            "bass": f"/download/processed/{title}/bass.wav",
            "drums": f"/download/processed/{title}/drums.wav",
            "piano": f"/download/processed/{title}/piano.wav",
            "other": f"/download/processed/{title}/other.wav",
        }

        return render_template('result.html', links=download_links)

    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/download/<path:folder>/<path:filename>', methods=['GET'])
def download(folder, filename):
    """
    Serves the requested file for download.
    """
    directory = UPLOAD_FOLDER if folder == "uploads" else PROCESSED_FOLDER
    return send_from_directory(directory=directory, path=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
