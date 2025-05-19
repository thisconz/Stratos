# Stratos

Cloud Storage & Document Intelligence Platform.

---

## 📦 Structure

- `backend/` – FastAPI backend (user auth, file storage, analytics)
- `frontend/` – Coming soon (Next.js + Tailwind UI)

---

## 🚀 Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
