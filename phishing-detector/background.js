chrome.runtime.onInstalled.addListener(() => {
  console.log("Phishing Detector extension installed!");
});

// Example: listen for tab updates
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete") {
    console.log("Tab updated:", tab.url);
  }
});
