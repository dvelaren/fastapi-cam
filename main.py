import cv2, threading, time
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

app = FastAPI()

camera = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_lock = threading.Lock()
current_frame = None


def capture_loop():
    global current_frame
    while True:
        success, frame = camera.read()
        if not success:
            time.sleep(0.1)
            continue
        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            continue
        with frame_lock:
            current_frame = buffer.tobytes()


# Start the capture thread
threading.Thread(target=capture_loop, daemon=True).start()


def generate_frames():
    while True:
        with frame_lock:
            frame = current_frame
        if frame is None:
            time.sleep(0.05)
            continue
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        time.sleep(0.05)  # control frame rate (~20 FPS)


@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(
        generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/")
async def index():
    # Simple HTML page with an <img> tag streaming the video
    return Response(
        content="""
    <html>
        <body>
            <h2>Webcam Stream</h2>
            <img src="/video_feed" width="640" height="480">
        </body>
    </html>
    """,
        media_type="text/html",
    )
