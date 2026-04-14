document.querySelectorAll("a").forEach(link => {
  if (link.href.includes("suspicious.com")) {
    link.style.border = "2px solid red";
    link.title = "⚠️ Potential phishing link detected!";
  }
});
