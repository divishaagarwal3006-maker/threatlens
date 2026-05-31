import requests
import re
import os
from urllib.parse import urlparse

API_KEY = os.environ.get("GOOGLE_API_KEY")

# ─────────────────────────────────────────
# 1. HEURISTIC URL SCORING
# ─────────────────────────────────────────
def heuristic_score(url: str) -> int:
    score = 0

    keywords = ["login", "verify", "update", "password", "secure",
                "click", "account", "banking", "confirm", "suspend",
                "paypal", "amazon", "apple", "google", "microsoft",
                "signin", "sign-in", "log-in", "logon", "auth",
                "authenticate", "validation", "validate", "recover",
                "reset", "unlock", "reactivate", "billing", "invoice",
                "payment", "refund", "transaction", "alert", "notice",
                "security", "token", "session", "credential", "access"]
    for word in keywords:
        if word in url.lower():
            score += 30

    if "@" in url:
        score += 50
    if len(url) > 75:
        score += 30

    suspicious_tlds = [".biz", ".info", ".tk", ".ml", ".ga", ".cf",
                       ".gq", ".xyz", ".top", ".club", ".online",
                       ".site", ".website", ".fun", ".space", ".icu",
                       ".live", ".buzz", ".click", ".link", ".win"]
    for tld in suspicious_tlds:
        if url.lower().endswith(tld) or tld + "/" in url.lower():
            score += 20

    if re.match(r'https?://\d+\.\d+\.\d+\.\d+', url):
        score += 50

    try:
        domain = urlparse(url).netloc
        if domain.count('.') > 3:
            score += 30
    except:
        pass

    lookalikes = ["paypa1", "arnazon", "g00gle", "micros0ft",
                  "faceb00k", "app1e", "netfl1x", "y0utube",
                  "twitterr", "linkedln", "instagrarr", "whatsaap",
                  "paypai", "amaz0n", "gooogle", "micosoft",
                  "facbook", "youtub", "instagam", "twiter"]
    for fake in lookalikes:
        if fake in url.lower():
            score += 60

    try:
        domain = urlparse(url).netloc
        if domain.count('-') >= 2:
            score += 25
    except:
        pass

    if not url.startswith("https://"):
        score += 20

    return min(score, 100)


# ─────────────────────────────────────────
# 2. EMAIL MODEL SCORING (EXPANDED)
# ─────────────────────────────────────────
def email_model_score(text: str) -> int:
    score = 0
    text_lower = text.lower()

    # ── CRITICAL RISK PHRASES (+40 each) ──
    critical_risk = [
        "your account has been suspended",
        "your account has been compromised",
        "your account will be terminated",
        "verify your account immediately",
        "confirm your identity now",
        "you have been selected as a winner",
        "claim your prize now",
        "you won a lottery",
        "send us your bank details",
        "provide your credit card number",
        "wire transfer required",
        "your ssn is needed",
        "your social security number",
        "irs tax refund",
        "you owe back taxes",
        "legal action will be taken",
        "arrest warrant issued",
        "fbi investigation",
        "your computer has a virus",
        "call this number immediately",
        "nigerian prince",
        "inheritance funds",
        "million dollars waiting",
        "bitcoin investment guaranteed",
        "double your money",
    ]
    for phrase in critical_risk:
        if phrase in text_lower:
            score += 40

    # ── HIGH RISK PHRASES (+30 each) ──
    high_risk = [
        "suspended", "click here", "verify your account",
        "update your payment", "unusual activity", "confirm your identity",
        "your account has been", "limited access", "immediately",
        "action required", "urgent", "winner", "you have been selected",
        "account locked", "account disabled", "account suspended",
        "security alert", "security breach", "unauthorized access",
        "suspicious login", "suspicious activity detected",
        "your password has expired", "reset your password now",
        "validate your email", "validate your account",
        "reactivate your account", "your subscription has expired",
        "payment failed", "billing issue", "update billing",
        "refund pending", "unclaimed refund", "tax refund",
        "you have a pending transaction",
        "click the link below", "click the button below",
        "act now", "act immediately", "respond immediately",
        "final warning", "last chance", "expires today",
        "expires in 24 hours", "limited time offer",
        "free gift", "free iphone", "free amazon gift card",
        "congratulations you won", "lucky winner",
        "kindly provide", "kindly confirm", "kindly verify",
        "dear valued customer", "dear account holder",
    ]
    for phrase in high_risk:
        if phrase in text_lower:
            score += 30

    # ── MEDIUM RISK PHRASES (+15 each) ──
    medium_risk = [
        "password", "login", "bank", "credit card",
        "social security", "dear customer", "dear user",
        "username", "sign in", "log in", "authenticate",
        "otp", "one time password", "verification code",
        "pin number", "cvv", "expiry date", "card number",
        "bank account", "routing number", "swift code",
        "western union", "moneygram", "wire transfer",
        "paypal account", "apple id", "google account",
        "microsoft account", "amazon account", "netflix account",
        "your order", "package delivery", "delivery failed",
        "parcel waiting", "shipment notification",
        "invoice attached", "payment receipt",
        "tax return", "government grant", "stimulus check",
        "crypto", "cryptocurrency", "bitcoin", "ethereum",
        "investment opportunity", "high returns guaranteed",
        "work from home", "earn money online", "passive income",
        "lose weight fast", "miracle cure", "doctor approved",
        "click unsubscribe", "remove me", "opt out",
    ]
    for phrase in medium_risk:
        if phrase in text_lower:
            score += 15

    # ── LOW RISK PHRASES (+8 each) ──
    low_risk = [
        "dear", "free", "offer", "discount", "sale",
        "buy now", "order now", "shop now", "limited",
        "exclusive", "special", "bonus", "reward",
        "prize", "gift", "earn", "money", "cash",
        "income", "profit", "investment", "opportunity",
        "risk free", "no cost", "100%", "guaranteed",
        "click", "link", "visit", "open", "download",
        "attachment", "attached", "see below",
    ]
    for phrase in low_risk:
        if phrase in text_lower:
            score += 8

    # ── GRAMMAR / STYLE RED FLAGS (+10 each) ──
    grammar_flags = [
        "kindly do the needful",
        "revert back to us",
        "do the needful",
        "please to inform",
        "we are waiting your",
        "as soon as possible kindly",
        "your good self",
    ]
    for phrase in grammar_flags:
        if phrase in text_lower:
            score += 10

    # ── SUSPICIOUS SENDER PATTERNS (+20) ──
    suspicious_patterns = [
        r'noreply@(?!.*\.(com|org|net|gov|edu)$)',
        r'support@[a-z0-9\-]+\.(tk|ml|ga|cf|gq|xyz)',
        r'admin@[a-z0-9\-]+\.(tk|ml|ga|cf|gq|xyz)',
    ]
    for pattern in suspicious_patterns:
        if re.search(pattern, text_lower):
            score += 20

    # ── URLs found in email body ──
    urls_in_text = re.findall(r'http[s]?://\S+', text)
    for url in urls_in_text:
        score += heuristic_score(url) // 2

    # ── EXCESSIVE CAPS (+10) ──
    words = text.split()
    if len(words) > 5:
        caps_ratio = sum(1 for w in words if w.isupper() and len(w) > 2) / len(words)
        if caps_ratio > 0.3:
            score += 10

    # ── EXCESSIVE EXCLAMATION (+10) ──
    if text.count('!') >= 3:
        score += 10

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
        return 0


# ─────────────────────────────────────────
# 4. FINAL COMBINED SCORE
# ─────────────────────────────────────────
def final_score(input_text: str, is_url: bool = False) -> int:
    if is_url:
        h_score = heuristic_score(input_text)
        sb_score = safe_browsing_score(input_text)
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
# 6. ANALYZE FUNCTION
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