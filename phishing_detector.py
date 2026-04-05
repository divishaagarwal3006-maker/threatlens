
import requests

API_KEY = "AIzaSyBfrepWDDFJICUA01sP4nSkJsqhJFIwPn4"  # replace with your real key

def heuristic_score(url: str) -> int:
    score = 0
    # suspicious keywords
    keywords = ["login", "verify", "update", "password", "secure", "click", "account"]
    for word in keywords:
        if word in url.lower():
            score += 30

    # @ symbol in URL
    if "@" in url:
        score += 50

    # very long URL
    if len(url) > 75:
        score += 30

    # suspicious TLDs (cheap domains often used in scams)
    suspicious_tlds = [".biz", ".info", ".net"]
    for tld in suspicious_tlds:
        if url.lower().endswith(tld):
            score += 20

    return score


def email_model_score(text: str) -> int:
    # placeholder: you can load your trained model here
    if "suspended" in text.lower() or "click here" in text.lower():
        return 90
    return 20

def safe_browsing_score(url: str) -> int:
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
    body = {
        "client": {"clientId": "phishing-detector", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    response = requests.post(endpoint, json=body)
    data = response.json()
    return 100 if "matches" in data else 0

def final_score(input_text: str, is_url: bool = False) -> int:
    if is_url:
        # combine heuristic + Safe Browsing
        score = heuristic_score(input_text)
        score += safe_browsing_score(input_text)
        return min(score, 100)  # cap at 100
    else:
        return email_model_score(input_text)
