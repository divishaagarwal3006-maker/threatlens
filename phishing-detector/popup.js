document.getElementById("results").innerText = "Scanning current page...";

// Example: send message to content script
chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
  chrome.scripting.executeScript({
    target: {tabId: tabs[0].id},
    func: () => {
      return [...document.querySelectorAll("a")].map(a => a.href);
    }
  }, (results) => {
    const links = results[0].result;
    let suspicious = links.filter(l => l.includes("suspicious.com"));
    document.getElementById("results").innerHTML =
      suspicious.length > 0
        ? `<span class="suspicious">⚠️ Found suspicious links!</span>`
        : `<span class="safe">✅ No suspicious links detected.</span>`;
  });
});
