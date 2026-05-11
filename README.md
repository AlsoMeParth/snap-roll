# SNAP-ROLL: AI-Powered Smart Attendance System 

SNAP-ROLL is an advanced AI-powered attendance system designed to streamline classroom management through biometric verification. Built with Streamlit and backed by a Supabase database, the system provides a seamless experience for both teachers and students using state-of-the-art face and voice recognition technologies.

---

## 🔗 Project Links
* **Landing Page:** https://snap-roll-landing-page.vercel.app/
* **Live Application:** https://snap-roll.streamlit.app/

## 🚀 Key Features
* **Dual Portal System:** Dedicated interfaces for Teachers and Students backed by a Supabase database.
* **Face Recognition:** Uses dlib's ResNet CNN for embeddings and Scikit-learn SVC for high-accuracy identification.
* **Voice Recognition:** Employs Resemblyzer and librosa for speaker identification via classroom recordings.
* **Smart Caching:** Optimized performance using `st.cache_resource` to manage heavy ML models and database connections.
* **Real-time Analytics:** Automated attendance logging with relational database management using PostgreSQL.

## 🛠️ Tech Stack 
| Component | Technology |
| :--- | :--- |
| **Frontend / UI** | Streamlit |
| **Face Recognition** | dlib + face_recognition_models (ResNet CNN) |
| **Face Classifier** | Scikit-learn SVC (linear kernel) |
| **Voice Recognition** | Resemblyzer (VoiceEncoder) + librosa |
| **Database** | Supabase (PostgreSQL) |
| **Caching** | st.cache_resource |

## 📂 Project Structure
Based on the repository architecture:
```text
SNAP-ROLL/
├── .streamlit/
├── src/
│   ├── components/            # UI components and dialogs
│   │   ├── dialog_add_photo.py
│   │   ├── dialog_attendance_res...
│   │   ├── dialog_auto_enroll.py
│   │   ├── dialog_share_subject.py
│   │   ├── dialog_student_enroll...
│   │   ├── dialog_voice_attenda...
│   │   ├── footer.py
│   │   ├── header.py
│   │   ├── subject_card.py
│   │   └── teacher_subject_dialo...
│   ├── database/              # Database configuration and logic
│   │   ├── config.py
│   │   └── db.py
│   ├── img/                   # Assets and logos
│   │   └── logo.png
│   ├── pipelines/             # Core AI logic (Face & Voice)
│   │   ├── face_pipeline.py
│   │   └── voice_pipeline.py
│   ├── screens/               # Main application pages
│   │   ├── home_screen.py
│   │   ├── student_screen.py
│   │   └── teacher_screen.py
│   └── ui/                    # Layout and styling
│       └── base_layout.py
├── venv/                      # Virtual environment
├── .gitignore
├── app.py                     # Application entry point
└── requirements.txt           # Project dependencies