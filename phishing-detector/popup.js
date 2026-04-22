document.getElementById("scanBtn").addEventListener("click", async () => {
  // Get the current tab
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  let url = tab.url;

  // Call your backend
  try {
    let response = await fetch("http://127.0.0.1:5000/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });

    let data = await response.json();

    // Show result in popup
    document.getElementById("result").textContent =
      `Risk: ${data.risk} | Reason: ${data.reason}`;
  } catch (err) {
    document.getElementById("result").textContent = "Error: " + err.message;
  }
});
