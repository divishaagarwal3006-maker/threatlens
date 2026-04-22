# 🛡️ ThreatLens — AI-Powered Phishing & Malware Detection

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

ThreatLens is an AI-powered phishing and malware detection system that
analyzes URLs and emails in real time using machine learning,
heuristics, and Google Safe Browsing API.

---

## 🚀 Features

- 🔍 **URL Scanning** — Detects phishing URLs using heuristics + Google Safe Browsing API
- 📧 **Email Analysis** — ML model trained to detect phishing emails
- 🌐 **Browser Extension** — Real-time scanning directly in Edge/Chrome
- 📊 **Streamlit Dashboard** — Visual interface for analysis
- ⚡ **Flask API** — Backend REST API for predictions
- 🎯 **3-Level Risk Scoring** — SAFE / SUSPICIOUS / PHISHING

---

## 📁 Project Structure
---
hreatlens/
├── 📂 phishing-detector/        # Browser Extension
│   ├── manifest.json            # Extension config (Manifest V3)
│   ├── popup.html               # Extension popup UI
│   ├── popup.js                 # Popup logic
│   ├── background.js            # Service worker
│   ├── content.js               # Page content scanner
│   └── icons/                   # Extension icons
│
├── api_server.py                # Flask REST API
├── app.py                       # Streamlit dashboard
├── phishing_detector.py         # Core detection engine
├── train_email_model.py         # ML model training
├── email_model.pkl              # Trained ML model
├── emails.csv                   # Training dataset
└── requirements.txt             # Python dependencies

## 🌐 Browser Extension Setup

### Install in Edge / Chrome

1. Open `edge://extensions` or `chrome://extensions`
2. Enable **Developer Mode**
3. Click **Load Unpacked**
4. Select the `phishing-detector/` folder
5. ThreatLens icon appears in toolbar ✅

### How it works
- Click the **ThreatLens** icon on any webpage
- Click **Scan Current Tab**
- Get instant risk assessment: 🟢 SAFE / 🟡 SUSPICIOUS / 🔴 PHISHING

---

## ⚙️ Backend Setup

### 1. Clone the repo
```bash
git clone https://github.com/divishaagarwal3006-maker/threatlens.git
cd threatlens
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Flask API
```bash
python api_server.py
```

### 4. Start Streamlit Dashboard
```bash
streamlit run app.py
```

---

## 🔬 How Detection Works

| Method | Weight | Description |
|--------|--------|-------------|
| Heuristic Analysis | 40% | Checks URL patterns, keywords, TLDs |
| Google Safe Browsing | 60% | Real-time threat database lookup |
| ML Email Model | 100% | Trained classifier for email text |

### Risk Levels
| Score | Level | Meaning |
|-------|-------|---------|
| 0–39 | 🟢 SAFE | No threats detected |
| 40–69 | 🟡 SUSPICIOUS | Proceed with caution |
| 70–100 | 🔴 PHISHING | Likely malicious |

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Streamlit
- **ML:** Scikit-learn, Pickle
- **Browser Extension:** JavaScript, Manifest V3
- **API:** Google Safe Browsing v4
- **Deployment:** Vercel (frontend)

---

## 👩‍💻 Author

**Divisha Agarwal**
[GitHub](https://github.com/divishaagarwal3006-maker)

---

## 📄 License

MIT License — feel free to use and modify!