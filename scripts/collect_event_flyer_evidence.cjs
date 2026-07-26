#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const { createWorker } = require("tesseract.js");

const ROOT = path.resolve(__dirname, "..");
const AGENDA = path.join(ROOT, "content", "events", "agenda-comunitaria-2026.json");
const DEFAULT_HTML = path.resolve(ROOT, "..", "jb-rider-eventos.html");
const DEFAULT_OUTPUT = path.join(ROOT, "content", "event-research", "flyer-ocr-evidence-2026.json");
const BASE_URL = "https://jb-rider.com.br/";

function argValue(name, fallback = null) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

function hasArg(name) {
  return process.argv.includes(name);
}

function cleanHtml(value) {
  return value
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<[^>]+>/g, "")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&nbsp;/g, " ")
    .trim();
}

function normalized(value) {
  return String(value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/\b(mc|mg|motoclube|moto clube)\b/g, " ")
    .replace(/[^a-z0-9]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function parseDate(value) {
  const match = value.match(/(\d{2})\/(\d{2})\/(\d{4})/);
  return match ? `${match[3]}-${match[2]}-${match[1]}` : "";
}

function parseCards(html) {
  const cards = [];
  const cardRegex = /<div class="col-lg-4 col-md-6 item-filtro">([\s\S]*?)(?=<div class="col-lg-4 col-md-6 item-filtro">|<\/div>\s*<\/div>\s*<script|$)/g;
  let match;
  while ((match = cardRegex.exec(html))) {
    const block = match[1];
    const strong = block.match(/<strong[^>]*>([\s\S]*?)<\/strong>/i);
    const image = block.match(/<img\s+src="([^"]+)"[^>]*alt="Flyer"/i);
    const video = block.match(/<source\s+src="([^"]+)"/i);
    const detail = block.match(/<a\s+href="(evento\/[^"]+)"/i);
    if (!strong) continue;
    const [dateLabel = "", label = ""] = cleanHtml(strong[1]).split("\n");
    const location = label.match(/^(.*)\s+-\s+(.+)-([A-Z]{2})$/);
    cards.push({
      date_label: dateLabel,
      start_date: parseDate(dateLabel),
      title: location ? location[1].trim() : label.trim(),
      city: location ? location[2].trim() : "",
      state: location ? location[3] : "",
      media_type: image ? "image" : video ? "video" : "none",
      media_url: image ? new URL(image[1], BASE_URL).href : video ? new URL(video[1], BASE_URL).href : null,
      detail_url: detail ? new URL(detail[1], BASE_URL).href : null,
    });
  }
  return cards;
}

function tokens(value) {
  return new Set(normalized(value).split(" ").filter(Boolean));
}

function similarity(left, right) {
  const a = tokens(left);
  const b = tokens(right);
  if (!a.size || !b.size) return 0;
  let intersection = 0;
  for (const token of a) if (b.has(token)) intersection += 1;
  return intersection / new Set([...a, ...b]).size;
}

function matchCard(event, cards) {
  const sameDateState = cards.filter(
    (card) =>
      card.start_date === event.start_date &&
      normalized(card.state) === normalized(event.state)
  );
  const sameCity = sameDateState.filter(
    (card) => normalized(card.city) === normalized(event.city)
  );
  const pool = sameCity.length ? sameCity : sameDateState;
  let best = null;
  for (const card of pool) {
    const titleScore = similarity(event.title, card.title);
    const combinedScore = similarity(
      `${event.title} ${event.city}`,
      `${card.title} ${card.city}`
    );
    const cityScore = normalized(card.city) === normalized(event.city) ? 0.25 : 0;
    const score = Math.max(titleScore + cityScore, combinedScore);
    if (!best || score > best.score) best = { card, score };
  }
  if (!best || best.score < 0.45) return null;
  return best;
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
    .slice(0, 8);
  return { times, phones, postal_codes: postalCodes, keywords, address_lines: addressLines };
}

async function recognizeAll(items, workerCount) {
  const workers = [];
  for (let index = 0; index < workerCount; index += 1) {
    workers.push(await createWorker("por"));
  }
  let cursor = 0;
  const results = new Array(items.length);
  async function run(worker) {
    while (true) {
      const index = cursor++;
      if (index >= items.length) return;
      const item = items[index];
      try {
        const response = await fetch(item.card.media_url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const buffer = Buffer.from(await response.arrayBuffer());
        const { data } = await worker.recognize(buffer);
        results[index] = {
          ...item,
          fetch_status: "ok",
          ocr_confidence: Math.round(data.confidence * 10) / 10,
          ocr_text: data.text.trim(),
          signals: extractSignals(data.text),
        };
      } catch (error) {
        results[index] = { ...item, fetch_status: "error", error: String(error) };
      }
      process.stdout.write(`OCR ${index + 1}/${items.length}: ${item.slug}\n`);
    }
  }
  await Promise.all(workers.map((worker) => run(worker)));
  await Promise.all(workers.map((worker) => worker.terminate()));
  return results;
}

async function main() {
  const htmlPath = path.resolve(argValue("--html", DEFAULT_HTML));
  const outputPath = path.resolve(argValue("--output", DEFAULT_OUTPUT));
  const limit = Number(argValue("--limit", "0"));
  const requestedSlugs = new Set(
    String(argValue("--slugs", ""))
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean)
  );
  const workerCount = Math.max(1, Number(argValue("--workers", "4")));
  const html = fs.readFileSync(htmlPath, "utf8");
  const cards = parseCards(html);
  const agenda = JSON.parse(fs.readFileSync(AGENDA, "utf8"));
  const pending = agenda.entries.filter((event) => !event.duplicate_of);
  const mapped = [];
  const unmatched = [];
  for (const event of pending) {
    const match = matchCard(event, cards);
    if (!match) {
      unmatched.push({
        slug: event.slug,
        title: event.title,
        start_date: event.start_date,
        city: event.city,
        state: event.state,
      });
      continue;
    }
    mapped.push({
      slug: event.slug,
      event_title: event.title,
      event_city: event.city,
      event_state: event.state,
      score: Math.round(match.score * 1000) / 1000,
      card: match.card,
    });
  }

  console.log(`Cards=${cards.length} Agenda=${pending.length} Mapeados=${mapped.length} SemCorrespondencia=${unmatched.length}`);
  if (hasArg("--map-only")) {
    if (hasArg("--output")) {
      fs.mkdirSync(path.dirname(outputPath), { recursive: true });
      fs.writeFileSync(
        outputPath,
        JSON.stringify(
          {
            generated_at: new Date().toISOString(),
            source_url: "https://jb-rider.com.br/eventos.php",
            cards_found: cards.length,
            agenda_active_entries: pending.length,
            mapped_entries: mapped,
            unmatched_entries: unmatched,
          },
          null,
          2
        ) + "\n",
        "utf8"
      );
      console.log(`Inventário gravado: ${outputPath}`);
    }
    for (const item of unmatched.slice(0, 100)) {
      console.log(`SEM_MAPA ${item.start_date} | ${item.slug}`);
    }
    return;
  }

  const imageItems = mapped.filter(
    (item) =>
      item.card.media_type === "image" &&
      (!requestedSlugs.size || requestedSlugs.has(item.slug))
  );
  const selected = limit > 0 ? imageItems.slice(0, limit) : imageItems;
  const evidence = await recognizeAll(selected, workerCount);
  const payload = {
    generated_at: new Date().toISOString(),
    source_url: "https://jb-rider.com.br/eventos.php",
    source_html: path.basename(htmlPath),
    cards_found: cards.length,
    agenda_active_entries: pending.length,
    mapped_entries: mapped.length,
    unmatched_entries: unmatched,
    non_image_mapped_entries: mapped.filter((item) => item.card.media_type !== "image"),
    ocr_entries: evidence,
  };
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(payload, null, 2) + "\n", "utf8");
  console.log(`Evidências gravadas: ${outputPath} (${evidence.length} flyers)`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
