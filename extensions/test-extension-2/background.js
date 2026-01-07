chrome.action.onClicked.addListener(async () => {
  const payload = { message: "Hello from Chrome extension!", when: new Date().toISOString() };
  try {
    const resp = await fetch("http://127.0.0.1:8000/collect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    console.log("Server said:", await resp.text());
  } catch (e) {
    console.error("Fetch failed:", e);
  }
});
