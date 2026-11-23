# 🚀 AI Career Copilot

An AI-powered career guidance and resume analysis web application built with **Python (Flask)**, **Groq LLM API**, and **TiDB Cloud (MySQL)**. Users can upload or paste their resume, specify a target job role, and receive instant skill gap analysis, a personalized learning roadmap, and tailored mock interview questions.

---

## ✨ Key Features

- **Multi-Format Resume Parsing:** Supports direct text input as well as `.pdf` (`PyPDF2`) and `.docx` (`python-docx`) file uploads.
- **Dynamic AI Model Routing:** Automatically fetches and selects the best active text model via the Groq API (`client.models.list()`) to prevent downtime from model deprecations.
- **Structured Career Insights (JSON Mode):**
  - ✅ **Extracted Skills:** Identifies existing technical and soft skills from the resume.
  - 🔍 **Skill Gap Analysis:** Highlights missing skills required for the target role.
  - 🗺️ **Actionable Roadmap:** Generates a step-by-step learning plan to bridge the gap.
  - 🎯 **Mock Interview Questions:** Provides role-specific interview questions based on the candidate's profile.
- **User Authentication & Report History:** Secure signup/login system with persistent cloud storage (TiDB MySQL via SQLAlchemy) to review past resume analyses anytime.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, SQLAlchemy
- **AI Engine:** Groq API (Dynamic LLM Selection with Structured JSON Output)
- **Database:** TiDB Cloud (MySQL) with SSL (`PyMySQL`, `certifi`)
- **Frontend:** HTML5, CSS3, Jinja2 Templates
- **Document Processing:** `PyPDF2`, `python-docx`

---

## 📂 Project Structure

```text
AI-Career-Copilot/
├── app.py              # Main Flask application & routes
├── ai.py               # Groq API integration & dynamic model selection
├── db.py               # TiDB Cloud MySQL database connection
├── models.py           # SQLAlchemy User & Reports schemas
├── requirements.txt    # Project dependencies
├── .gitignore          # Ignored environment & cache files
├── static/
│   └── style.css       # Application styling
└── templates/
    ├── base.html
    ├── login.html
    ├── signup.html
    ├── dashboard.html
    └── history.html
