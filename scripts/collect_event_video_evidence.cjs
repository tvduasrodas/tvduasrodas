#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { createWorker } = require("tesseract.js");

const ROOT = path.resolve(__dirname, "..");
const INVENTORY = path.join(ROOT, "content", "event-research", "event-source-inventory-2026-v2.json");
const OUTPUT = path.join(ROOT, "content", "event-research", "video-ocr-evidence-2026.json");
const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

function normalized(value) {
  return String(value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function extractSignals(rawText) {
  const text = rawText.replace(/\r/g, "");
  const times = [...new Set(
    [...text.matchAll(/\b(?:[01]?\d|2[0-3])(?:[:hH]\s?[0-5]\d|[hH])\b/g)].map((item) => item[0])
  )];
  const phones = [...new Set(
    [...text.matchAll(/(?:\(?\d{2}\)?\s*)?(?:9\s*)?\d{4}[-.\s]?\d{4}/g)].map((item) => item[0].trim())
  )];
  const postalCodes = [...new Set(
    [...text.matchAll(/\b\d{5}-?\d{3}\b/g)].map((item) => item[0])
  )];
  const keywords = [
    "estacionamento", "parking", "camping", "chuveiro", "café da manhã",
    "entrada franca", "gratuito", "gratuita", "ingresso", "alimento",
    "praça de alimentação", "food", "rock", "show", "banda", "expositor",
    "acessórios", "troféu", "sorteio", "wheeling", "motocross"
  ].filter((keyword) => normalized(text).includes(normalized(keyword)));
  const addressLines = text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => /\b(rua|r\.|avenida|av\.|rodovia|rod\.|praça|praca|estrada|km|parque)\b/i.test(line))
    .slice(0, 12);
  return { times, phones, postal_codes: postalCodes, keywords, address_lines: addressLines };
}

async function screenshotFrame(page, videoUrl, fraction) {
  await page.setContent(
    `<style>html,body{margin:0;background:#000}video{width:1080px;height:1080px;object-fit:contain}</style>` +
    `<video id="v" muted playsinline preload="auto" src="${videoUrl.replace(/"/g, "&quot;")}"></video>`
  );
  await page.waitForFunction(() => {
    const video = document.querySelector("#v");
    return video && Number.isFinite(video.duration) && video.duration > 0 && video.readyState >= 1;
  }, null, { timeout: 30000 });
  await page.evaluate(async (fractionValue) => {
    const video = document.querySelector("#v");
    const target = Math.max(0, Math.min(video.duration - 0.1, video.duration * fractionValue));
    await new Promise((resolve) => {
      video.addEventListener("seeked", resolve, { once: true });
      video.currentTime = target;
    });
  }, fraction);
  return page.locator("#v").screenshot({ type: "png" });
}

async function main() {
  const inventory = JSON.parse(fs.readFileSync(INVENTORY, "utf8"));
  const items = inventory.mapped_entries.filter((item) => item.card.media_type === "video");
  const browser = await chromium.launch({ headless: true, executablePath: CHROME });
  const workers = [await createWorker("por"), await createWorker("por")];
  let cursor = 0;
  const results = new Array(items.length);

  async function run(worker) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1080 } });
    while (true) {
      const index = cursor++;
      if (index >= items.length) break;
      const item = items[index];
      try {
        const texts = [];
        const confidences = [];
        for (const fraction of [0.15, 0.5, 0.85]) {
          const image = await screenshotFrame(page, item.card.media_url, fraction);
          const { data } = await worker.recognize(image);
          texts.push(data.text.trim());
          confidences.push(data.confidence);
        }
        const rawText = [...new Set(texts)].filter(Boolean).join("\n\n--- QUADRO ---\n\n");
        results[index] = {
          ...item,
          fetch_status: "ok",
          inspected_frames: [0.15, 0.5, 0.85],
          ocr_confidence: Math.round((confidences.reduce((a, b) => a + b, 0) / confidences.length) * 10) / 10,
          ocr_text: rawText,
          signals: extractSignals(rawText),
        };
      } catch (error) {
        results[index] = { ...item, fetch_status: "error", error: String(error) };
      }
      process.stdout.write(`VIDEO ${index + 1}/${items.length}: ${item.slug}\n`);
    }
    await page.close();
  }

  await Promise.all(workers.map((worker) => run(worker)));
  await Promise.all(workers.map((worker) => worker.terminate()));
  await browser.close();
  fs.writeFileSync(
    OUTPUT,
    JSON.stringify(
      {
        generated_at: new Date().toISOString(),
        source_url: inventory.source_url,
        inspected_videos: results.length,
        ocr_entries: results,
      },
      null,
      2
    ) + "\n",
    "utf8"
  );
  console.log(`Evidências de vídeo gravadas: ${OUTPUT}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
