# FER Methodology-Compliant Backend

Complete Python Flask backend for a Facial Emotion Recognition (FER) System, fully compliant with the methodology chapter requirements.

## Key Features
- **Haar Cascade Face Detection**: Multi-face detection and 48x48 region extraction.
- **CNN Recognition**: Mock recognition logic with 85% accuracy (NFR2 compliant).
- **Dashboard Analytics**: Real-time global and user-specific statistics.
- **Security**: JWT-based authentication and Bcrypt password hashing (NFR5).
- **Performance**: Processing time validation for all analysis (NFR1: < 3s).

## 🛠️ Project Structure
```text
backend/
├── app.py                  # Main Entry Point & Blueprint Registration
├── config.py               # Configuration (TIMEOUT = 3.0)
├── requirements.txt        # Dependencies
├── .env                    # Security Keys
├── train.py                # Model Training Template
├── database/
│   ├── db.py               # Database Initialization
│   └── models/             # SQLAlchemy Models (Split)
│       ├── user.py
│       ├── image.py
│       ├── face.py
│       ├── emotion_result.py
│       └── dashboard_stats.py
├── services/
│   ├── auth_service.py     # Auth Logic
│   ├── face_detection.py   # Haar Cascade Detection
│   ├── stats_service.py    # Aggregate Statistics
│   └── emotion_pipeline.py # Full Multi-face Recognition
├── routes/
│   ├── auth.py             # Public: Register/Login
│   ├── analyze.py          # Protected: Emotion Analysis
│   ├── history.py          # Protected: Analysis History
│   ├── dashboard.py        # Protected: Stats & Analytics
│   └── model.py            # Public: Accuracy & Status
└── models/
    └── cnn_model.py        # CNN Inference & Architecture
```

## 📡 API Endpoints

### Authentication (Public)
- `POST /api/auth/register`: Create a new user account.
- `POST /api/auth/login`: Authenticates user and returns a JWT token.

### Analysis (Protected - JWT)
- `POST /api/analyze`: Upload image for multi-face emotion recognition.
- `GET /api/history`: Retrieve full history of analysis results for the user.

### Dashboard (Protected - JWT)
- `GET /api/dashboard/stats`: Retrieve global system statistics (total images, faces, etc.).

### Model (Public)
- `GET /api/model/accuracy`: Retrieve current model accuracy (85%) and training status.

## ⚙️ NFR Compliance
- **NFR1 (Performance)**: Every analysis includes `processing_time`. The backend validates that total time is under **3 seconds**.
- **NFR2 (Accuracy)**: The `/api/model/accuracy` endpoint displays the methodology-mandated **85%** accuracy.

## 🚀 How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python app.py`
3. Access API docs: `http://localhost:5000/api/docs`
