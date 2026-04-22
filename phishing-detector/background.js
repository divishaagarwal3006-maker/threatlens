chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {
    fetch("http://127.0.0.1:5000/scan", {   // swap with Vercel URL later
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: tab.url })
    })
    .then(res => res.json())
    .then(data => {
      if (data.isMalicious) {
        chrome.action.setBadgeText({ text: "!", tabId });
        chrome.action.setBadgeBackgroundColor({ color: "red", tabId });
      } else {
        chrome.action.setBadgeText({ text: "✔", tabId });
        chrome.action.setBadgeBackgroundColor({ color: "green", tabId });
      }
    })
    .catch(err => console.error("Scan error:", err));
  }
});
