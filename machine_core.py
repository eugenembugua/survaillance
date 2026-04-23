import cv2, torch, faiss, sqlite3, numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

class MachineIntelligence:
    def __init__(self):
        print(f"[*] Booting Neural Engine on {DEVICE}...")
        self.mtcnn = MTCNN(keep_all=True, device=DEVICE)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(DEVICE)
        
        # Identity Indices
        try:
            self.index = faiss.read_index("govt.index")
        except:
            self.index = None

        # Global Active Search Target
        self.active_target_vec = None
        self.active_target_name = None

    def set_active_target(self, pil_image, name="POI"):
        """Acquires a new target from an uploaded image."""
        # MTCNN crops and aligns the face from the upload
        face = self.mtcnn(pil_image)
        if face is not None:
            # Generate the unique biometric signature
            emb = self.resnet(face[0].unsqueeze(0)).detach().cpu().numpy()
            faiss.normalize_L2(emb)
            self.active_target_vec = emb
            self.active_target_name = name
            return True
        return False

    def process_frame(self, frame, camera_id):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes, _ = self.mtcnn.detect(rgb)
        faces = self.mtcnn(rgb)
        
        if faces is None: return frame

        # Batched processing for all faces in frame
        batch = torch.stack(faces).to(DEVICE)
        embs = self.resnet(batch).detach().cpu().numpy()
        faiss.normalize_L2(embs)

        for i, emb in enumerate(embs):
            label, color = "UNKNOWN", (255, 255, 255)
            
            # 1. PRIORITY: Check against Active Manhunt Target
            if self.active_target_vec is not None:
                similarity = np.dot(emb, self.active_target_vec.flatten())
                if similarity > 0.82: # Alert threshold
                    label = f"TARGET ACQUIRED: {self.active_target_name}"
                    color = (0, 0, 255) # RED
                    # Trigger alert (In production, this would fire a webhook/SMS)
                    print(f"[!] {label} detected at {camera_id}")

            # 2. SECONDARY: General database match
            elif self.index:
                D, I = self.index.search(np.array([emb]), k=1)
                if float(D[0][0]) > 0.85:
                    label = f"AUTHORIZED: {int(I[0][0])}"
                    color = (0, 255, 0)

            # UI Rendering
            x1, y1, x2, y2 = map(int, boxes[i])
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
        return frame