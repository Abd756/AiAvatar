# AI Avatar - Guided Self-Reflection Platform 🧘‍♂️🎭

An AI-powered platform for guided therapeutic self-reflection. The system uses a specialized decision engine ("The Brain") to guide users through structured reflection scripts using a warm, compassionate AI avatar.

---

## 🏗️ Project Architecture

Current tech stack:
- **Frontend**: Next.js 15 (React), Tailwind CSS, Framer Motion (Animations).
- **Backend**: FastAPI (Python), LangChain, Google Gemini 2.0 Flash.
- **Database**: Firebase Firestore (Session persistence & Dynamic Scripts).
- **Media**: Real-time pipeline preparation with Pipecat & Simli (In Progress).

---

## 📂 Project Structure

```text
AiAvatar/
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── routers/       # API Endpoints (sessions, scripts)
│   │   ├── services/      # Core logic (Brain, Script Manager, Firebase)
│   │   ├── schemas/       # Pydantic models (Data validation)
│   │   └── main.py        # Entry point
│   └── scripts/           # Local therapeutic scripts (Fallback)
├── frontend/               # Next.js Application
│   ├── src/
│   │   ├── components/    # UI Components (ChatInterface, etc.)
│   │   ├── services/      # Frontend API client
│   │   └── app/           # Next.js pages & layout
├── testing/                # Standalone verification scripts
├── firebase_service_key.json # Firebase Credentials (Keep Private)
├── .env                    # Environment variables
└── requirements.txt        # Python dependencies
```

---

## 🛠️ Local Setup

### 1. Backend Setup
1. **Navigate to backend**:
   ```bash
   cd e:\AsapStudio\AiAvatar
   ```
2. **Create & Activate Virtual Environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**:
   Create a `.env` file in the root with:
   ```env
   GEMINI_API_KEY=your_key
   OPENAI_API_KEY=your_key (optional)
   # FIREBASE_SERVICE_KEY_BASE64=... (optional, used for production)
   ```
5. **Run Server**:
   ```bash
   python -m backend.app.main
   ```
   The backend will run at `http://localhost:8000`.

### 2. Frontend Setup
1. **Navigate to frontend**:
   ```bash
   cd e:\AsapStudio\AiAvatar\frontend
   ```
2. **Install Dependencies**:
   ```bash
   npm install
   ```
3. **Configure Environment Variables**:
   Create `frontend/.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
   ```
4. **Run Development Server**:
   ```bash
   npm run dev
   ```
   The frontend will run at `http://localhost:3000`.

---

## 🌟 Core Features

- **Dynamic Script Selection**: Choose from various reflection themes (Daily Check-In, Morning Reflection, Gratitude Journal) stored in Firestore.
- **Decision Engine (The Brain)**: Advanced decision logic ensures the AI follows therapeutic rules (NEXT, REASK, ACKNOWLEDGE) without giving advice.
- **Session Persistence**: Sessions are saved in Firestore, allowing for stateful conversations.
- **Safety Re-asks**: Enforces meaningful depth by asking users to elaborate if their responses are too brief.
- **Premium UI**: Dark-mode support, soft gradients, and interactive animations for a therapeutic feel.

---

## 🚀 Deployment

For production deployment instructions, please refer to the [Deployment Guide](C:/Users/abdul/.gemini/antigravity/brain/3326997b-b8b1-4bfc-814d-e6f501a15f86/deployment_guide.md).

- **Backend**: Deployed on **Render**.
- **Frontend**: Deployed on **Vercel**.
