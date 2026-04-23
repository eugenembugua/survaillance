# Survaillance Prototype

A high-performance, distributed biometric surveillance system inspired by the "Person of Interest" architecture. This system performs real-time face detection, biometric encoding, and **active target manhunts** across multiple camera nodes.

## System Architecture
The system operates on a decentralized **Sovereign Intelligence** model:

1.  **The Watchtower (Nodes):** Background camera workers that perform MTCNN detection and batched InceptionResNetV1 encoding.
2.  **The Brain (API Server):** A FastAPI-based central command that manages active targets and broadcasts neural data via WebSockets.
3.  **The Console (Dashboard):** A Streamlit-based tactical interface for real-time monitoring and POI (Person of Interest) acquisition.



## Tactical Components
- `api_server.py`: The central nervous system. Manages camera workers and target distribution.
- `machine_core.py`: The neural engine. Handles biometric fingerprints and manhunt triggers.
- `dashboard.py`: The operator's terminal. Used to upload targets and view live feeds.
- `auth.py`: The secure ledger. Logs all operator actions and target sightings.
- `enroll.py`: Used to seed the system with a "Government Database" of known identities.

## Deployment Guide

### Environment Setup
Install the neural frameworks and high-speed communication layers:
```bash
pip install torch torchvision facenet-pytorch opencv-python faiss-cpu streamlit fastapi uvicorn websockets requests pillow

Enrollment (Initial Seeding)
Place images of known citizens in /govt_db (format: Name.jpg) and run the enrollment tool to generate the biometric memory:

Bash
python enroll.py

Engaging the Engine
Start the central API server. This will automatically initiate the camera nodes:

Bash
uvicorn api_server:app --host 0.0.0.0 --port 8000

Tactical Monitoring
Launch the dashboard to monitor feeds and initiate manhunts:

Bash
streamlit run dashboard.py

Core Capabilities

Active Target Acquisition (Manhunt Mode)
Operators can upload a photo of a Person of Interest (POI) via the dashboard. The system extracts facial landmarks and distributes a 512-dimensional biometric signature to every node. Every camera feed then scans specifically for this target.
Zero-Lag Streaming
By utilizing WebSockets and asynchronous Python, the system bypasses traditional UI bottlenecks. The neural engine processes frames in the background and pushes them directly to the console for a fluid, real-time experience.
Secure Audit Ledger
All system interactions—including camera views and target acquisitions—are recorded in a persistent SQLite database (intel.db) for forensic accountability.

Ethical Disclosure
This prototype is designed for educational purposes and localized security research. It demonstrates the technical capabilities of modern surveillance. Operators must ensure compliance with local privacy laws and data protection regulations before deployment.
