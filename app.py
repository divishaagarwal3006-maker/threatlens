import streamlit as st
import requests
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, ThreatLens!"


st.set_page_config(
    page_title="ThreatLens – PhishGuard AI",
    page_icon="🛡️",
    layout="wide"
)


st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b1f3a; /* dark blue */
        color: white;
    }
    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #081a2b !important;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

        /* Risk level badges */
        .high-risk {
            background-color: #FF0000; /* Red */
            color: red ;
            padding: 6px 12px;
            border-radius: 8px;
            font-weight: bold;
            box-shadow: 0 0 10px #FF0000;
        }
        .medium-risk {
            background-color: #FFA500; /* Orange */
            color: black;
            padding: 6px 12px;
            border-radius: 8px;
            font-weight: bold;
            box-shadow: 0 0 10px #FFA500;
        }
        .low-risk {
            background-color: #FFFF00; /* Yellow */
            color: black;
            padding: 6px 12px;
            border-radius: 8px;
            font-weight: bold;
            box-shadow: 0 0 10px #FFFF00;
        }
        .safe-risk {
            background-color: #00FF00; /* Green */
            color: black;
            padding: 6px 12px;
            border-radius: 8px;
            font-weight: bold;
            box-shadow: 0 0 10px #00FF00;
        }
        stTabs [role="tab"] {
            background-color: #001f4d; /* Navy shade */
            color: white;
            border-radius: 6px;
            padding: 8px;
            margin-right: 6px;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            background-color: #004080; /* Highlighted dark blue */
            font-weight: bold;
            box-shadow: 0 0 8px #00FFFF;
        }

        /* Buttons */
        .stButton>button {
            background-color: #004080;
            color: white;
            border-radius: 6px;
            border: none;
            padding: 8px 16px;
            font-weight: bold;
            box-shadow: 0 0 8px #00FFFF;
        }
        .stButton>button:hover {
            background-color: #0066cc;
            box-shadow: 0 0 12px #00FFFF;
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.sidebar.title("Detection Engines")
st.sidebar.write("• Heuristic / Lexical Analysis — always active")
st.sidebar.write("• Google Safe Browsing — Active")

st.sidebar.title("Risk Levels")
st.sidebar.markdown("🔴 **HIGH** — Score ≥ 80")
st.sidebar.markdown("🟠 **MEDIUM** — Score 60–79")
st.sidebar.markdown("🟡 **LOW** — Score 30–59")
st.sidebar.markdown("🟢 **SAFE** — Score < 30")

st.sidebar.title("About")
st.sidebar.info("ThreatLens combines lexical heuristics with the Google Safe Browsing API to detect malicious URLs in real time.")
tab1, tab2, tab3 = st.tabs(["Single URL Scan", "Batch URL Scan", "Email Scan"])

with tab1:
    url = st.text_input("Enter a URL to scan", key="single_url")
    if st.button("Scan URL", key="scan_single"):
        response = requests.post("http://localhost:5000/scan_url", json={"url": url})
        result = response.json()
        st.subheader(f"Risk Level: {result['risk']} | Score: {result['score']}/100")

        # NEW: Show reason
        st.write(f"Reason: {result['reason']}")

        if result['risk'] == "HIGH":
            st.error("Google Safe Browsing: Threat detected!")
        else:
            st.success("Google Safe Browsing: No threats found.")

with tab2:
    urls = st.text_area("Paste multiple URLs (one per line)", key="batch_urls")
    if st.button("Scan Batch", key="scan_batch"):
        for u in urls.splitlines():
            response = requests.post("http://localhost:5000/scan_url", json={"url": u})
            result = response.json()
            if result['risk'] == "HIGH":
                st.error(f"{u} → HIGH ({result['score']}) | Reason: {result['reason']}")
            elif result['risk'] == "MEDIUM":
                st.warning(f"{u} → MEDIUM ({result['score']}) | Reason: {result['reason']}")
            elif result['risk'] == "LOW":
                st.info(f"{u} → LOW ({result['score']}) | Reason: {result['reason']}")
            else:
                st.success(f"{u} → SAFE ({result['score']}) | Reason: {result['reason']}")

with tab3:
    email_text = st.text_area("Paste Email Text", key="email_input")
    if st.button("Scan Email", key="scan_email"):
        response = requests.post("http://localhost:5000/scan_email", json={"text": email_text})
        result = response.json()
        st.subheader(f"Email classified as → {result['risk']} ({result['score']})")

        # NEW: Show reason
        st.write(f"Reason: {result['reason']}")

        if result['risk'] == "HIGH":
            st.error("Suspicious email content detected!")
        else:
            st.success("No phishing indicators found.")


col1, col2 = st.columns([2,1])
with col1:
    urls = st.text_area("Paste URLs (one per line)", key="url_input")
with col2:
    if st.button("Scan URLs", key="scan_button"):
        if urls:
            for url in urls.splitlines():
                response = requests.post(
                    "http://localhost:5000/scan_url",
                    json={"url": url}
                )
                result = response.json()

                # Color-coded results + reason
                if result['risk'] == "HIGH":
                    st.error(f"{result['url']} → HIGH ({result['score']}) | Reason: {result['reason']}")
                elif result['risk'] == "MEDIUM":
                    st.warning(f"{result['url']} → MEDIUM ({result['score']}) | Reason: {result['reason']}")
                elif result['risk'] == "LOW":
                    st.info(f"{result['url']} → LOW ({result['score']}) | Reason: {result['reason']}")
                else:
                    st.success(f"{result['url']} → SAFE ({result['score']}) | Reason: {result['reason']}")


