
# 🤖 Smart ATS

**Smart ATS** is a Streamlit-based web application that uses **Google's Gemini API** to evaluate resumes against job descriptions — just like a real Applicant Tracking System (ATS).  
It helps job seekers **improve their resumes** with smart, AI-powered, targeted feedback and a beautifully clean visual UI.

---

## Features

- 📌 **Resume Parsing**: Upload a PDF and extract the raw text
- 📋 **JD Matching**: Paste any job description for context
- 📊 **Matching Percentage**: See how well your resume aligns
- 🧠 **Profile Summary**: AI-generated, concise summary of your strengths
- 🔍 **Missing Keywords**: Identify skills and terms missing from your resume
- 💡 **Detailed Evaluation**: Educational, project, and skill-based feedback
- 🎨 **Beautiful UI**: Visually enhanced with color-coded sections and emoji icons

---

## Tech Stack

- [Streamlit](https://streamlit.io/)
- [Google Gemini API (generativeai)](https://ai.google.dev/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- `st.secrets` for secure API key management

---

## 📂 Project Structure

```

smart-ats/
├── app.py               # Main Streamlit app
├── requirements.txt     # Required Python packages
├── .gitignore           # Ignore .env and virtual env
└── .env (local only)    # Contains your Gemini API key (not pushed to GitHub)

````

---

## Secrets & API Key Setup

This app uses the **Google Gemini API**. To keep your key safe:

1. **Do not** push your `.env` file to GitHub  
2. Instead, add the key to **Streamlit Cloud** under `Advanced Settings → Secrets`:

```toml
# .streamlit/secrets.toml
GOOGLE_API_KEY = "your-real-gemini-api-key"
````

In Python code:

```python
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
```

---

## Local Development

To run this project locally:

```bash
# Clone the repo
git clone https://github.com/SowmyaNihitha/smart-ats.git
cd smart-ats

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🌐 Live Demo

My app is live at:
🔗 [https://smart-ats-scan.streamlit.app/](https://smart-ats-scan.streamlit.app/)

---

## Author

Made with ❤️ by **Sowmya Nihitha Nadimpalli**
This project is part of a portfolio initiative to build impactful tools for job seekers.

---

## 📜 License

This project is open-source and available under the **MIT License**.

