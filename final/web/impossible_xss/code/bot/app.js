import puppeteer from "puppeteer";
import express from "express";
import rateLimit from "express-rate-limit";
import fs from "fs";

function resolveExecutable() {
  const candidates = [
    process.env.PUPPETEER_EXECUTABLE_PATH,
    process.env.CHROMIUM_PATH,
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/google-chrome",
  ].filter(Boolean);

  for (const candidate of candidates) {
    try {
      if (fs.existsSync(candidate)) {
        return candidate;
      }
    } catch (e) {
      console.warn(`[-] Error checking browser path ${candidate}: ${e.message}`);
    }
  }

  console.warn("[!] No Chromium executable found, falling back to default Puppeteer binary");
  return null;
}

const executablePath = resolveExecutable();
if (executablePath) {
  console.log(`[+] Using Chromium executable: ${executablePath}`);
}

const app = express();
app.use(express.json());
app.set("trust proxy", 1);

app.use(
  "/visit",
  rateLimit({
    windowMs: 3 * 60 * 1000,
    max: 5,
    message: { error: "Too many requests, try again later" },
  })
);

const port = process.env.PORT || 3001;
const APP_URL = process.env.APP_URL || "http://web/";
const FLAG = process.env.FLAG || "CTF{fake_flag}";

console.log(`FLAG: ${FLAG}`);
console.log(`APP_URL: ${APP_URL}`);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function allowedHost(targetUrl) {
  try {
    const baseline = new URL(APP_URL);
    const candidate = targetUrl instanceof URL ? targetUrl : new URL(targetUrl);
    return (
      baseline.hostname === candidate.hostname &&
      (baseline.port === candidate.port || (!baseline.port && !candidate.port))
    );
  } catch (e) {
    return false;
  }
}

function canonicalizeForNavigation(targetUrl) {
  const candidate = targetUrl instanceof URL ? targetUrl : new URL(targetUrl);
  const adjustedSearch = candidate.search ? candidate.search.replace(/\+/g, "%2B") : "";
  return `${candidate.origin}${candidate.pathname}${adjustedSearch}${candidate.hash}`;
}

async function visit(displayUrl, navUrl) {
  let browser = null;
  let ctx = null;
  try {
    const launchOptions = {
      headless: "new",
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--disable-gpu",
      ],
    };

    if (executablePath) {
      launchOptions.executablePath = executablePath;
    }

    browser = await puppeteer.launch(launchOptions);

    ctx = await browser.createIncognitoBrowserContext();

    const page = await ctx.newPage();
    await page.goto(APP_URL, { waitUntil: "networkidle2", timeout: 20000 });

    await sleep(1000);

    await page.setCookie({
      name: "flag",
      value: FLAG,
      url: APP_URL,
      path: "/",
      httpOnly: false,
      sameSite: "Lax",
    });

    await page.close();

    const attackPage = await ctx.newPage();
    await attackPage.goto("about:blank");

    await attackPage.goto(navUrl, { waitUntil: "networkidle2", timeout: 20000 });

    await sleep(5000);

    let docCookie = "";
    try {
      docCookie = await attackPage.evaluate(() => document.cookie);
    } catch (e) {
      docCookie = `error:${String(e)}`;
    }

    console.log(`[+] Visited ${displayUrl}, document.cookie=${docCookie}`);

    await attackPage.close();
  } catch (err) {
    console.error("visit error:", err);
  } finally {
    try { if (ctx) await ctx.close(); } catch {}
    try { if (browser) await browser.close(); } catch {}
    console.log(`[*] Done visiting -> ${displayUrl}`);
  }
}

app.get("/visit", async (req, res) => {
  const { url } = req.query;
  if (typeof url !== "string" || !url || !url.startsWith("http")) {
    return res.status(400).send({ error: "Invalid url" });
  }

  let targetUrl;
  try {
    targetUrl = new URL(url);
  } catch (e) {
    return res.status(400).send({ error: "Invalid url" });
  }

  if (!allowedHost(targetUrl)) {
    return res.status(403).send({ error: "url not allowed" });
  }

  try {
    const navUrl = canonicalizeForNavigation(targetUrl);
    console.log(`[*] Visiting -> ${navUrl}`);
    visit(targetUrl.toString(), navUrl);
    return res.sendStatus(200);
  } catch (e) {
    console.error(`[-] Error visiting -> ${url}: ${e.message}`);
    return res.status(400).send({ error: e.message });
  }
});

app.listen(port, async () => {
  console.log(`[*] Listening on port ${port}`);
});
