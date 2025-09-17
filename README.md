# fastapi-cam

A simple FastAPI application for streaming live video from a webcam using OpenCV.

## Features

- Streams video from a webcam (`/dev/video0`) in MJPEG format
- Web interface to view the live stream
- REST endpoint for direct video feed consumption

## Requirements

- Python 3.12+
- Linux (uses `/dev/video0` for webcam)

## Installation

1. **Clone the repository:**
   ```zsh
   git clone https://github.com/dvelaren/fastapi-cam.git
   cd fastapi-cam
   ```
2. **(Recommended) Create a virtual environment:**
   ```zsh
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```zsh
   pip install -r requirements.txt
   # or, if using pyproject.toml:
   pip install .
   ```
   Or with [uv](https://github.com/astral-sh/uv):
   ```zsh
   uv sync
   ```

## Usage

Start the FastAPI server:

```zsh
uv run fastapi run app/main.py --host 0.0.0.0 --port 9999
```

Or with Docker Compose:

```zsh
docker-compose up -p fastapi-cam --build -d
```

- Open your browser and go to [http://localhost:9999](http://localhost:9999) to view the webcam stream.
- The video feed is available at [http://localhost:9999/video_feed](http://localhost:9999/video_feed) as an MJPEG stream.

## Project Structure

- `./app/main.py` — Main FastAPI application
- `pyproject.toml` — Project metadata and dependencies

## Endpoints

- `/` — Web page with embedded video stream
- `/video_feed` — MJPEG video stream endpoint

## Notes

- The app uses `/dev/video0` as the webcam source. Change this in `./app/main.py` if needed.
- Make sure your user has permission to access the webcam device.
- Tested on Linux. For Windows/Mac, camera device path and OpenCV backend may need adjustment.

## License

MIT
