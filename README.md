# 🛡 CyberGuard AI

CyberGuard AI is an AI-powered Cybersecurity Threat Intelligence Web Application that analyzes cybersecurity threats, generates structured risk reports, and visualizes organizational security posture using interactive dashboards.

It combines a multi-agent LLM pipeline with analytics and role-based access control to simulate an enterprise-grade cybersecurity monitoring system.

---

## 🚀 Features

### 🔐 Authentication System
- Secure Login & Signup
- Password hashing
- Role-based access (User / Admin)
- Organization-based user management

### 🤖 AI-Powered Threat Analyzer
- Multi-agent pipeline (Researcher → Analyst → Reporter)
- Structured cybersecurity intelligence reports
- Risk scoring system (0–25 scale)
- Risk level classification (Low / Medium / High / Critical)
- Downloadable PDF reports

### 📡 Threat Feed
- Displays historical analyzed threats
- Sorted by timestamp
- Sector-based filtering

### 📊 Advanced Analytics Dashboard
- Monthly Risk Trend (Line Graph)
- Threat Distribution by Sector (Pie Chart)
- Risk by Sector (Bar Graph)
- Risk Heatmap (Sector vs Month)
- Organization Security Score KPI

### 🎯 Action Center
- Automated alert classification
- Critical / High / Monitoring status indicators

### 👑 Admin Dashboard
- Role-based access control
- Organization-level user visibility
- Restricted admin-only dashboard access

---

## 🏗 Architecture Overview

The system follows a layered architecture:

### 1️⃣ AI Processing Layer
- Multi-agent system using CrewAI
- LLM integration (Groq / Ollama / Mistral / Phi3)
- Structured threat analysis pipeline

### 2️⃣ Backend Layer
- SQLite database
- Stores users, roles, reports, and risk scores

### 3️⃣ Analytics Layer
- Plotly-based visualizations
- KPI and risk metrics generation

### 4️⃣ Frontend Layer
- Built using Streamlit
- Interactive dashboards and navigation

---

## 🧠 How It Works

1. User enters a cybersecurity threat query.
2. Multi-agent AI pipeline analyzes the threat.
3. Risk score is calculated.
4. Structured report is generated.
5. Report is saved in database.
6. Dashboard updates with analytics and visualizations.

---

## 🛠 Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Backend logic & AI integration |
| Streamlit | Web application framework |
| CrewAI | Multi-agent orchestration |
| LLM (Groq/Ollama) | Threat intelligence analysis |
| SQLite | Database management |
| Plotly | Data visualization |
| ReportLab | PDF report generation |
| Werkzeug | Secure password hashing |

---

## 📦 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/cyberguard-ai.git
cd cyberguard-ai

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\Activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Application
streamlit run app.py

🔐 Default Behavior

First registered user becomes super_admin

Role-based dashboard protection

Admin page accessible only to users with admin role

📊 Risk Model

Risk Score Range: 0–25

Security Score Formula:

Security Score = 100 - (Average Risk × 3)

Higher risk reduces organizational security score.

📌 Future Enhancements

Real-time threat API integration

Email alert notifications

Advanced ML-based anomaly detection

Multi-organization super admin panel

AWS cloud deployment

Subscription-based SaaS model

🎯 Project Type

This is an AI-powered Enterprise Cybersecurity Intelligence Web Application designed as a SaaS prototype.

👩‍💻 Developed By

Jayati Kandula
B.Tech – Information Technology
AI Enthusiast

📜 License

This project is for academic and research purposes.


