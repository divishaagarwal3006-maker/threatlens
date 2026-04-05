import streamlit as st
import requests

st.set_page_config(
    page_title="ThreatLens – PhishGuard AI",
    page_icon="🛡️",
    layout="wide"
)


st.markdown(
    """
    <style>
    body {
        background-color: #121212;   /* Dark background */
        color: #e0e0e0;              /* Light text */
    }
    .stButton>button {
        background-color: #0f4c75;   /* Custom button color */
        color: white;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
    }
    .stTextInput>div>input, .stTextArea>div>textarea {
        background-color: #1b262c;
        color: #bbe1fa;
        border-radius: 5px;
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


