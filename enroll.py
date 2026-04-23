import cv2, base64, asyncio, numpy as np
from fastapi import FastAPI, WebSocket
from machine_core import MachineIntelligence

app = FastAPI()
machine = MachineIntelligence()
clients = {}

async def broadcast(camera_id, frame):
    _, buffer = cv2.imencode(".jpg", frame)
    data = base64.b64encode(buffer).decode()
    if camera_id in clients:
        for ws in clients[camera_id]:
            try: await ws.send_text(data)
            except: clients[camera_id].remove(ws)

async def camera_worker(camera_id, src):
    cap = cv2.VideoCapture(src)
    while True:
        ret, frame = cap.read()
        if not ret: await asyncio.sleep(1); continue
        processed = machine.process_frame(frame, camera_id)
        await broadcast(camera_id, processed)
        await asyncio.sleep(0.02) # Cap at ~50FPS

@app.websocket("/ws/{camera_id}")
async def ws_endpoint(websocket: WebSocket, camera_id: str):
    await websocket.accept()
    clients.setdefault(camera_id, []).append(websocket)
    try:
        while True: await asyncio.sleep(1)
    except: clients[camera_id].remove(websocket)

@app.on_event("startup")
async def start_nodes():
    # ADD ANY CAMERA SOURCE HERE FOR EXPANSION
    CAMERAS = {"LOBBY_01": 0} 
    for cam_id, src in CAMERAS.items():
        asyncio.create_task(camera_worker(cam_id, src))