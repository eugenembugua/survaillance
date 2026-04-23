import streamlit as st
import websocket, threading, base64, requests
from PIL import Image

st.set_page_config(layout="wide", page_title="The Machine")
st.title("TACTICAL CONTROL INTERFACE")

# --- SIDEBAR: TARGET ACQUISITION ---
st.sidebar.header("Target Acquisition")
target_name = st.sidebar.text_input("Person of Interest Name")
uploaded_file = st.sidebar.file_uploader("Upload Profile Image", type=["jpg", "png"])

if st.sidebar.button("INITIATE MANHUNT"):
    if uploaded_file and target_name:
        files = {"file": uploaded_file.getvalue()}
        resp = requests.post(f"http://localhost:8000/acquire?name={target_name}", files={"file": uploaded_file})
        if resp.status_code == 200:
            st.sidebar.success(f"Scanning for {target_name}...")
        else:
            st.sidebar.error("Failed to acquire target.")

# --- MAIN: LIVE FEEDS ---
node = st.selectbox("Select Node", ["LOBBY_01"])
frame_placeholder = st.empty()

def stream_worker(node_id):
    ws = websocket.WebSocket()
    ws.connect(f"ws://localhost:8000/ws/{node_id}")
    while True:
        try:
            data = ws.recv()
            frame_placeholder.image(base64.b64decode(data), use_column_width=True)
        except: break

if st.button("ENGAGE SYSTEM"):
    threading.Thread(target=stream_worker, args=(node,), daemon=True).start()