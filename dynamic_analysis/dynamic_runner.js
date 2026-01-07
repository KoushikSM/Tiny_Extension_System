const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
 
async function attachNetworkLoggingToTarget(target, logFile) {
  try {
    const session = await target.createCDPSession();
    await session.send('Network.enable');
 
    session.on('Network.requestWillBeSent', (e) => {
      if (e.request) {
        fs.appendFileSync(logFile, `[REQ][${target.type()}] ${e.request.method} ${e.request.url}\n`);
        if (e.request.postData) {
          fs.appendFileSync(logFile, `  postData: ${e.request.postData}\n`);
        }
      }
    });
 
    session.on('Network.responseReceived', (e) => {
      fs.appendFileSync(logFile, `[RES][${target.type()}] ${e.response.status} ${e.response.url}\n`);
    });
  } catch (err) {
    // ignore targets that don't support Network domain
  }
}
 
(async () => {
  const extPath = "C:/Users/koushik/Documents/Extension/tiny-extension"; // adjust if needed
  const resultsDir = path.join(__dirname, "results", "network_logs");
  fs.mkdirSync(resultsDir, { recursive: true });
  const logFile = path.join(resultsDir, `log_${Date.now()}.txt`);
 
  const browser = await puppeteer.launch({
    headless: false,
    args: [
      `--disable-extensions-except=${extPath}`,
      `--load-extension=${extPath}`,
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ],
    defaultViewport: null
  });
 
  // Attach to existing targets
  const targets = await browser.targets();
  for (const t of targets) await attachNetworkLoggingToTarget(t, logFile);
 
  // Attach to any new targets (e.g., service worker starts)
  browser.on('targetcreated', async (t) => {
    await attachNetworkLoggingToTarget(t, logFile);
  });
 
  const page = await browser.newPage();
  await page.goto('https://example.com', { waitUntil: 'domcontentloaded' });
 
  // Give extension time to register service worker
  await new Promise(r => setTimeout(r, 2000));
 
  // Auto-trigger extension via keyboard (requires "commands" in manifest)
  console.log("⌨️ Triggering extension via Ctrl+Shift+Y");
  await page.bringToFront();
  await page.keyboard.down('Control');
  await page.keyboard.down('Shift');
  await page.keyboard.press('KeyY');
  await page.keyboard.up('Shift');
  await page.keyboard.up('Control');
 
  console.log("⏳ Watching network for 8s...");
  await new Promise(r => setTimeout(r, 8000));
 
  await browser.close();
  console.log(`📝 Network log saved to: ${logFile}`);
})();