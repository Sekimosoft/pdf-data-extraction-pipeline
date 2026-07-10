import { chromium } from "playwright";
import { mkdir, writeFile } from "fs/promises";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { tmpdir } from "os";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");

const BASE = process.env.SCREENSHOT_BASE ?? "https://pdf-extraction-web.onrender.com";
const API = process.env.SCREENSHOT_API ?? "https://pdf-extraction-api-9bub.onrender.com";

async function hydrate(page) {
  await page.goto(BASE, { waitUntil: "domcontentloaded", timeout: 120000 });
  await page.waitForTimeout(20000);
  await page.waitForSelector('input[type="file"]', { state: "attached", timeout: 60000 });
}

async function uploadPdf(page, filePath, extractLabel) {
  await page.locator('input[type="file"]').setInputFiles(filePath);
  await page.waitForTimeout(500);
  await page.getByRole("button", { name: extractLabel }).click();
}

async function captureInvoice(page, locale, suffix) {
  await hydrate(page);

  if (locale === "ja") {
    await page.getByRole("button", { name: "Switch language to Japanese" }).click();
    await page.waitForTimeout(800);
  }

  const sampleResp = await fetch(`${API}/api/v1/sample-pdf?locale=${locale}`);
  if (!sampleResp.ok) throw new Error(`Sample PDF fetch failed: ${sampleResp.status}`);
  const samplePath = join(tmpdir(), `sample-${suffix}.pdf`);
  await writeFile(samplePath, Buffer.from(await sampleResp.arrayBuffer()));

  const extractLabel = locale === "ja" ? "データを抽出" : "Extract data";
  const resultLabel = locale === "ja" ? "構造化請求書結果" : "Structured invoice result";

  await uploadPdf(page, samplePath, extractLabel);
  await page.getByText(resultLabel).waitFor({ timeout: 120000 });
  await page.waitForTimeout(800);

  await page.screenshot({
    path: `docs/screenshots/screenshot-${suffix}-structured.png`,
    fullPage: true,
  });
}

async function captureTextPreview(page) {
  await hydrate(page);

  const genericPath = join(ROOT, "backend/app/fixtures/generic_text.pdf");
  await uploadPdf(page, genericPath, "Extract data");
  await page.getByText("Text extraction preview").waitFor({ timeout: 120000 });
  await page.waitForTimeout(800);

  await page.screenshot({
    path: "docs/screenshots/screenshot-en-text-preview.png",
    fullPage: true,
  });
}

await mkdir("docs/screenshots", { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

await captureInvoice(page, "en", "en");
await captureInvoice(page, "ja", "ja");
await captureTextPreview(page);

await browser.close();
console.log("Screenshots saved to docs/screenshots/");
