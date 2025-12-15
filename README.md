🩺 Doctor AI Assistant

An AI-powered full-stack application that enables patients to book doctor appointments via natural language and allows doctors to receive automated daily reports via Slack.

Built using FastAPI + React + PostgreSQL + LLM tool calling.

🚀 Features
👤 Patient Side

Check doctor availability using natural language

Book appointments conversationally

Automatic email confirmation

Automatic Google Calendar event creation

🧑‍⚕️ Doctor Side

Ask natural language questions like:

“Give me today’s report”

“How many patients visited yesterday?”

Receive summary reports directly on Slack

Dashboard button support (frontend-triggered report)

🤖 AI Capabilities

LLM tool calling (availability, booking, reports)

Safe tool execution (no double booking)

Human-readable summaries from raw DB data

🏗️ Tech Stack
Backend

FastAPI

PostgreSQL (Neon)

SQLAlchemy

Groq LLM (LLaMA 3.1)

Google Calendar API

Gmail SMTP

Slack Incoming Webhooks

Frontend

React

Fetch API

Simple role-based UI (Patient / Doctor)

📁 Project Structure
doctor-ai-assistant/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes
│   │   ├── core/         # AI agent & prompts
│   │   ├── db/           # Models & database
│   │   ├── mcp/          # Tool functions
│   │   ├── services/     # Email, Calendar, Slack
│   │   └── utils/
│   ├── requirements.txt
│   └── .env              # Environment variables (NOT committed)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── api.js
│   │   ├── App.js
│   │   └── styles.css
│   └── package.json
│
└── README.md

⚙️ Environment Setup
🔐 Backend .env (create manually)

Create backend/.env with the following keys:

DATABASE_URL=postgresql://<user>:<password>@<host>/<db>?sslmode=require
GROQ_API_KEY=your_groq_api_key

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXX/YYYY/ZZZZ


⚠️ Important

.env is ignored by Git

Use Gmail App Password, not your real password

credentials.json & token.json (Google Calendar) are also ignored

▶️ Running the Project
1️⃣ Backend
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload


Backend runs at:
👉 http://127.0.0.1:8000

2️⃣ Frontend
cd frontend
npm install
npm start


Frontend runs at:
👉 http://localhost:3000

💬 Sample Prompts
🧑‍🦱 Patient
Check availability of Dr. Ram tomorrow
Book an appointment at 3:00 PM

🧑‍⚕️ Doctor
Give me today’s report
How many patients visited yesterday?


🔌 API Usage Summary
POST /chat

Request Body

{
  "user_role": "patient",
  "patient_name": "Patient1",
  "doctor_name": "Ram",
  "messages": [
    { "role": "user", "content": "Check availability of Dr. Ram tomorrow" }
  ]
}


Response

{
  "reply": "Dr. Ram is available tomorrow at 9:00 AM, 10:00 AM..."
}

🔔 Notifications

📧 Email → Sent to patients on booking confirmation

📅 Google Calendar → Event created automatically

💬 Slack → Doctor reports sent to configured channel

🧠 Key Design Decisions

Appointment booking is explicitly confirmed (safe flow)

LLM cannot directly create appointments

Backend validates availability before booking

Reports are aggregated via DB queries, not hallucinated
