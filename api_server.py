from flask import Flask, request, jsonify
from flask_cors import CORS
from phishing_detector import final_score

# 1. Create the Flask app object
app = Flask(__name__)
CORS(app)   # Enable CORS for all routes so the extension can fetch

# --- Extension-friendly route ---
@app.route("/scan", methods=["POST"])
def scan():
    """
    This route is used by the browser extension.
    It expects JSON: {"url": "<site_url>"}
    """
    data = request.json
    url = data.get("url", "")
    score = final_score(url, is_url=True)

    # Risk classification
    if score >= 80:
        risk = "HIGH"
        reason = "Phishing attempt detected: URL mimics a trusted site"
    elif score >= 60:
        risk = "MEDIUM"
        reason = "Suspicious patterns found: possible obfuscation or redirects"
    elif score >= 30:
        risk = "LOW"
        reason = "Minor anomalies detected but not strongly harmful"
    else:
        risk = "SAFE"
        reason = "No harmful indicators detected"

    return jsonify({
        "url": url,
        "score": score,
        "risk": risk,
        "reason": reason
    })

# --- Original routes for API use ---
@app.route("/scan_url", methods=["POST"])
def scan_url():
    data = request.json
    url = data.get("url", "")
    score = final_score(url, is_url=True)

    if score >= 80:
        risk = "HIGH"
        reason = "Phishing attempt detected: URL mimics a trusted site"
    elif score >= 60:
        risk = "MEDIUM"
        reason = "Suspicious patterns found: possible obfuscation or redirects"
    elif score >= 30:
        risk = "LOW"
        reason = "Minor anomalies detected but not strongly harmful"
    else:
        risk = "SAFE"
        reason = "No harmful indicators detected"

    return jsonify({
        "url": url,
        "score": score,
        "risk": risk,
        "reason": reason
    })

@app.route("/scan_email", methods=["POST"])
def scan_email():
    data = request.json
    text = data.get("text", "")
    score = final_score(text, is_url=False)

    if score >= 80:
        risk = "HIGH"
        reason = "Email contains phishing keywords and suspicious links"
    else:
        risk = "SAFE"
        reason = "No harmful indicators detected in email"

    return jsonify({
        "email_text": text,
        "score": score,
        "risk": risk,
        "reason": reason
    })

# 3. Run the server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
