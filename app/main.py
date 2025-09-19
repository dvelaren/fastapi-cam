import json
import cv2
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.requests import Request
from fastrtc import Stream
from pathlib import Path

cur_dir = Path(__file__).parent
app = FastAPI()


def camera_generator():
    camera = cv2.VideoCapture("/dev/video0")
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

    try:
        while True:
            success, frame = camera.read()

            if not success:
                break
            yield frame
    finally:
        camera.release()


# Create a WebRTC stream (video only, send-receive mode)
stream = Stream(
    handler=camera_generator,
    modality="video",
    mode="receive",
)

# Mount the WebRTC endpoint on FastAPI
stream.mount(app)


@app.get("/")
async def index():
    html = (cur_dir / "index.html").read_text()
    rtc_config = {}
    html = html.replace("__RTC_CONFIGURATION__", json.dumps(rtc_config))
    return HTMLResponse(html)


@app.post("/debug/echo")
async def debug_echo(request: Request):
    body = await request.body()
    response = JSONResponse(
        {
            "content_type": request.headers.get("content-type"),
            "body_length": len(body),
            "body_preview": body[:100].decode(errors="replace"),
        }
    )

    return response


if __name__ == "__main__":
    import os

    if (mode := os.getenv("MODE")) == "UI":
        print("Running using FastRTC UI")
        stream.ui.launch(server_port=7860)
    else:
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=7860)
