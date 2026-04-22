import requests
import re
from urllib.parse import urlparse

API_KEY = "AIzaSyBfrepWDDFJICUA01sP4nSkJsqhJFIwPn4"

# ─────────────────────────────────────────
# 1. HEURISTIC URL SCORING
# ─────────────────────────────────────────
def heuristic_score(url: str) -> int:
    score = 0

    # Suspicious keywords in URL
    keywords = ["login", "verify", "update", "password", "secure",
                "click", "account", "banking", "confirm", "suspend",
                "paypal", "amazon", "apple", "google", "microsoft"]
    for word in keywords:
        if word in url.lower():
            score += 30

    # @ symbol in URL (classic phishing trick)
    if "@" in url:
        score += 50

    # Very long URL
    if len(url) > 75:
        score += 30

    # Suspicious TLDs
    suspicious_tlds = [".biz", ".info", ".tk", ".ml", ".ga", ".cf", ".gq", ".xyz"]
    for tld in suspicious_tlds:
        if url.lower().endswith(tld) or tld + "/" in url.lower():
            score += 20

    # IP address used instead of domain name
    if re.match(r'https?://\d+\.\d+\.\d+\.\d+', url):
        score += 50

    # Too many subdomains (e.g. secure.login.verify.paypal.com.evil.com)
    try:
        domain = urlparse(url).netloc
        if domain.count('.') > 3:
            score += 30
    except:
        pass

    # Lookalike / typosquatted domains
    lookalikes = ["paypa1", "arnazon", "g00gle", "micros0ft",
                  "faceb00k", "app1e", "netfl1x", "y0utube"]
    for fake in lookalikes:
        if fake in url.lower():
            score += 60

    # Hyphen-heavy domains (e.g. secure-paypal-login-verify.com)
    try:
        domain = urlparse(url).netloc
        if domain.count('-') >= 2:
            score += 25
    except:
        pass

    # HTTPS missing
    if not url.startswith("https://"):
        score += 20

    return min(score, 100)  # cap at 100


# ─────────────────────────────────────────
# 2. EMAIL MODEL SCORING
# ─────────────────────────────────────────
def email_model_score(text: str) -> int:
    score = 0
    text_lower = text.lower()

    # High-risk phrases
    high_risk = [
        "suspended", "click here", "verify your account",
        "update your payment", "unusual activity", "confirm your identity",
        "your account has been", "limited access", "immediately",
        "action required", "urgent", "winner", "you have been selected"
    ]
    for phrase in high_risk:
        if phrase in text_lower:
            score += 30

    # Medium-risk phrases
    medium_risk = [
        "password", "login", "bank", "credit card",
        "social security", "dear customer", "dear user"
    ]
    for phrase in medium_risk:
        if phrase in text_lower:
            score += 15

    # Suspicious links in email body
    urls_in_text = re.findall(r'http[s]?://\S+', text)
    for url in urls_in_text:
        score += heuristic_score(url) // 2  # add partial URL score

    return min(score, 100)


# ─────────────────────────────────────────
# 3. GOOGLE SAFE BROWSING API
# ─────────────────────────────────────────
def safe_browsing_score(url: str) -> int:
    try:
        endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
        body = {
            "client": {
                "clientId": "phishing-detector",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION"
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        response = requests.post(endpoint, json=body, timeout=5)
        data = response.json()
        return 100 if "matches" in data else 0
    except Exception as e:
        print(f"[Safe Browsing API Error] {e}")
        return 0  # don't crash if API fails


# ─────────────────────────────────────────
# 4. FINAL COMBINED SCORE
# ─────────────────────────────────────────
def final_score(input_text: str, is_url: bool = False) -> int:
    if is_url:
        h_score = heuristic_score(input_text)
        sb_score = safe_browsing_score(input_text)

        # Weighted: Safe Browsing is more reliable
        combined = (h_score * 0.4) + (sb_score * 0.6)
        return min(int(combined), 100)
    else:
        return email_model_score(input_text)


# ─────────────────────────────────────────
# 5. RISK LABEL
# ─────────────────────────────────────────
def get_risk_label(score: int) -> dict:
    if score >= 70:
        return {
            "risk": "PHISHING",
            "level": "HIGH",
            "color": "red",
            "message": "⚠️ WARNING: This appears to be a phishing attempt!"
        }
    elif score >= 40:
        return {
            "risk": "SUSPICIOUS",
            "level": "MEDIUM",
            "color": "orange",
            "message": "⚠️ CAUTION: This URL/email looks suspicious."
        }
    else:
        return {
            "risk": "SAFE",
            "level": "LOW",
            "color": "green",
            "message": "✅ No harmful indicators detected."
        }


# ─────────────────────────────────────────
# 6. MAIN FUNCTION (called by api_server.py)
# ─────────────────────────────────────────
def analyze(input_text: str, is_url: bool = False) -> dict:
    score = final_score(input_text, is_url)
    label = get_risk_label(score)
    return {
        "score": score,
        "risk": label["risk"],
        "level": label["level"],
        "color": label["color"],
        "message": label["message"],
        "input": input_text,
        "type": "URL" if is_url else "EMAIL"
    }


# ─────────────────────────────────────────
# 7. QUICK LOCAL TEST
# ─────────────────────────────────────────
if __name__ == "__main__":
    test_url = "http://paypal-secure-login.verify-account.tk/update/password"
    test_email = "Dear user, your account has been suspended. Click here to verify immediately."

    print("=== URL TEST ===")
    result = analyze(test_url, is_url=True)
    print(result)

    print("\n=== EMAIL TEST ===")
    result = analyze(test_email, is_url=False)
    print(result)