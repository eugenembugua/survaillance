import cv2, base64, asyncio, io
from fastapi import FastAPI, WebSocket, UploadFile, File
from PIL import Image
from machine_core import MachineIntelligence
from auth import init_auth, log_action

app = FastAPI()
machine = MachineIntelligence()
clients = {}

async def broadcast(camera_id, frame):
    _, buffer = cv2.imencode(".jpg", frame)
    data = base64.b64encode(buffer).decode()
    if camera_id in clients:
        for ws in clients[camera_id][:]:
            try: await ws.send_text(data)
            except: clients[camera_id].remove(ws)

async def camera_worker(camera_id, src):
    cap = cv2.VideoCapture(src)
    while True:
        ret, frame = cap.read()
        if not ret: await asyncio.sleep(1); continue
        processed = machine.process_frame(frame, camera_id)
        await broadcast(camera_id, processed)
        await asyncio.sleep(0.03)

@app.post("/acquire")
async def acquire_target(name: str, file: UploadFile = File(...)):
    """API Endpoint to set a global manhunt target."""
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    if machine.set_active_target(image, name):
        log_action("ADMIN", f"Target Acquired: {name}")
        return {"status": "Active Search Initiated", "target": name}
    return {"status": "Error", "message": "No face detected in upload"}

@app.websocket("/ws/{camera_id}")
async def ws_endpoint(websocket: WebSocket, camera_id: str):
    await websocket.accept()
    clients.setdefault(camera_id, []).append(websocket)
    try:
        while True: await asyncio.sleep(1)
    except: clients[camera_id].remove(websocket)

@app.on_event("startup")
async def startup():
    init_auth()
    # Add camera nodes here
    asyncio.create_task(camera_worker("LOBBY_01", 0))