
# YouSplit Web App

A Flask-based web application that allows users to split audio tracks from YouTube videos into separate stems (e.g., vocals, bass, drums, piano, and others) using **Spleeter** and **yt-dlp**. Users can input a YouTube URL, and the app downloads the audio, processes it, and provides download links for the separated tracks.

---

## Features

- **YouTube Integration**: Fetch audio from YouTube videos using `yt-dlp`.
- **Audio Separation**: Separate audio into 5 distinct stems using `Spleeter`.
- **Downloadable Files**: Provides direct download links for the original audio and separated tracks.

---

## Prerequisites

- **Python**: Version 3.9 or higher
- **Docker** (Optional): For containerized deployment
- **ffmpeg**: Required for audio processing (automatically installed in Docker image)

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/audio-splitter.git
cd audio-splitter
```

### Set Up the Environment

1. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install `ffmpeg`**:
   - On Linux: `sudo apt-get install ffmpeg`
   - On macOS: `brew install ffmpeg`
   - On Windows: [Download ffmpeg](https://ffmpeg.org/download.html) and add it to your PATH.

---

## Running the Application

### Local Development

1. Start the Flask app:
   ```bash
   python app.py
   ```

2. Open your browser and visit:
   ```
   http://localhost:5000
   ```

### Docker Deployment

1. **Build the Docker image**:
   ```bash
   docker build -t yousplit .
   ```

2. **Run the container**:
   ```bash
   docker run -p 5000:5000 yousplit
   ```

3. Access the app at:
   ```
   http://localhost:5000
   ```
---

## Project Structure

```
audio-splitter/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── templates/             # HTML templates
│   ├── index.html         # Home page
│   ├── result.html        # Results page with download links
├── static/                # Static files
│   └── css/
│       └── style.css      # Stylesheet for the application
├── uploads/               # (Generated) Directory for downloaded YouTube audio
├── processed/             # (Generated) Directory for processed audio stems
└── README.md              # Project README
```

---

## Technologies Used

- **Flask**: Backend web framework
- **Spleeter**: Audio source separation library by Deezer
- **yt-dlp**: YouTube video downloader
- **ffmpeg**: Audio processing library

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- **[Deezer](https://github.com/deezer/spleeter)** for the amazing Spleeter library.
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** for YouTube downloading support.
