# Face Emotion Intelligence

A production-ready MVP that combines a FastAPI backend, ONNXRuntime-powered inference services, and a React PWA frontend for face detection, identity recognition, and emotion classification in real time.

## Features
- Real-time webcam analysis with overlay visualisations (bounding boxes, identity, emotion).
- Photo upload workflow with drag-and-drop support and latency feedback.
- Enrollment workflow for creating local identity embeddings stored in SQLite.
- Configurable recognition threshold and top-k controls for experimentation.
- PWA install experience with offline caching for static assets.
- Docker Compose stack with Nginx reverse proxy for unified deployment.

## Screenshots
> Replace the images below with actual screenshots captured from the running application.

![Live screen placeholder](docs/screens/live.png)
![Enrollment screen placeholder](docs/screens/enroll.png)

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (optional but recommended for production parity)

### Environment variables
Copy `deploy/.env.example` to `.env` and adjust as required.

```bash
cp deploy/.env.example .env
```

Key variables:
- `EMBEDDING_THRESHOLD` – default similarity threshold for recognition.
- `DB_URL` – SQLAlchemy connection string (default SQLite).
- `LOG_LEVEL` – backend logging level.
- `VITE_API_BASE_URL` – frontend API base URL.

### Local Development

1. **Install dependencies**
   ```bash
   make install-backend
   make install-frontend
   ```
2. **Start backend**
   ```bash
   make dev-backend
   ```
3. **Start frontend**
   ```bash
   make dev-frontend
   ```
4. Open the frontend at http://localhost:5173. API docs are available at http://localhost:8000/docs.

### Docker Compose

Single command build and run:
```bash
make run
```
The stack exposes:
- Frontend via Nginx at http://localhost:8080
- FastAPI backend directly at http://localhost:8000

Stop the stack with `docker compose down`.

## Architecture

```text
+---------------------+        +-----------------------+
|  React PWA (Vite)   | <----> |  Nginx Reverse Proxy  |
+---------------------+        +----------+------------+
           |                              |
           | REST /api                    |
           v                              v
+---------------------+        +-----------------------+
|   FastAPI Backend   |<------>|  SQLite / Embeddings  |
|  Detection & ML via |        +-----------------------+
|    ONNXRuntime      |
+---------------------+
```

### Backend Service Layout
```
backend/
  app.py                 # FastAPI application setup
  dependencies.py        # Lazy-loaded singleton services
  routers/               # Route handlers (/detect, /pipeline, /enroll, ...)
  services/              # ML orchestration (detector, embedder, emotions, storage)
  utils/                 # Pre/post processing, metrics, logging
  db/                    # SQLAlchemy models and session helpers
  models/                # Placeholder ONNX weights (replace with real models)
  tests/                 # Pytest suites covering API and pipeline flow
```

### Frontend Layout
```
frontend/
  src/
    pages/               # Live, Photo, Enroll, About views
    components/          # CameraView, EmotionBar, overlays, dialogs
    api/                 # Axios client wrappers
    pwa/                 # Service worker (TypeScript reference)
    styles/              # Global styles
  public/                # Manifest, service worker, icons
```

## API Reference

### `GET /api/health`
Returns service status and version.

### `POST /api/detect`
Accepts multipart or base64 encoded images and returns detected face bounding boxes and landmarks.

### `POST /api/recognize`
Runs detection + embedding similarity matching. Response example:
```json
[
  {
    "person": "Jane Doe",
    "similarity": 0.71,
    "embedding_norm": 1.02,
    "bbox": [120, 80, 180, 180],
    "score": 0.97
  }
]
```

### `POST /api/emotion`
Returns a ranked set of emotion probabilities per detected face.

### `POST /api/pipeline`
Full detection → recognition → emotion flow. Example response:
```json
{
  "faces": [
    {
      "bbox": [120, 80, 180, 180],
      "landmarks": {
        "l_eye": [138, 122],
        "r_eye": [210, 120],
        "nose": [175, 152],
        "l_mouth": [150, 192],
        "r_mouth": [200, 188]
      },
      "score": 0.98,
      "identity": { "person": "Ivan Petrov", "similarity": 0.72 },
      "emotion": {
        "label": "happy",
        "probabilities": {
          "neutral": 0.02,
          "happy": 0.9,
          "sad": 0.01,
          "angry": 0.01,
          "surprise": 0.03,
          "fear": 0.02,
          "disgust": 0.01
        }
      }
    }
  ],
  "timing_ms": { "total": 165, "detect": 41, "embed": 55, "recognize": 10, "emotion": 39 }
}
```

### `POST /api/enroll`
Enroll a new person using one or more base64 encoded images. Response includes the new person ID and number of samples used.

### `GET /api/persons`
List enrolled identities with pagination metadata.

### `DELETE /api/persons/{id}`
Remove an identity and its embeddings from storage.

## Testing & Quality

Run backend unit tests:
```bash
make test
```

Run linters:
```bash
make lint
```

CI recommendation: run `make test` and `make lint` inside your pipeline to ensure code quality.

## Performance Notes
- Frames are throttled to ~4 FPS (250 ms interval) in the live camera view.
- Images are resized to max 640px client-side before transmission to limit payload size.
- ONNXRuntime CPU execution is used by default; replace the placeholder `.onnx` files with production models for best results.

## Ethical Guidelines
- Obtain explicit consent before enrolling individuals.
- Communicate system limitations and potential biases in facial recognition and emotion inference.
- Provide a workflow to delete enrolled profiles (implemented via `/api/persons/{id}`).

## License & Models
This project ships with placeholder ONNX model files. Replace them with licensed models compliant with your deployment context. All application code is provided under the MIT license (adjust as needed).
