(function () {
    "use strict";

    const DEFAULT_IMAGE = "/assets/img/competicoes-eventos-default.svg";
    const statusLabels = {
        em_andamento: "Em andamento",
        proximo: "Próximo",
        agendada: "Agendada",
        concluida: "Concluída",
        encerrado: "Encerrado",
        cancelado: "Cancelado"
    };

    const esc = (value) => String(value ?? "")
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;").replace(/'/g, "&#39;");

    function safeUrl(value, fallback = "#") {
        const raw = String(value || "").trim();
        if (!raw) return fallback;
        if (/^\/(?!\/)|^[a-z0-9][a-z0-9._/-]*$/i.test(raw)) return raw;
        try {
            const url = new URL(raw, window.location.origin);
            return ["http:", "https:"].includes(url.protocol) ? url.href : fallback;
        } catch (_) {
            return fallback;
        }
    }

    function dateFromIso(value) {
        if (!value) return null;
        const parts = value.slice(0, 10).split("-").map(Number);
        if (parts.length !== 3 || parts.some(Number.isNaN)) return null;
        return new Date(parts[0], parts[1] - 1, parts[2]);
    }

    function formatDate(value, options = {}) {
        const date = dateFromIso(value);
        if (!date) return value || "A confirmar";
        return new Intl.DateTimeFormat("pt-BR", {
            day: "2-digit", month: options.long ? "long" : "short", year: "numeric"
        }).format(date);
    }

    function formatRange(start, end) {
        if (!start) return "Data a confirmar";
        if (!end || start === end) return formatDate(start, { long: true });
        const a = dateFromIso(start);
        const b = dateFromIso(end);
        if (!a || !b) return `${formatDate(start)} a ${formatDate(end)}`;
        if (a.getMonth() === b.getMonth() && a.getFullYear() === b.getFullYear()) {
            return `${a.getDate()} a ${new Intl.DateTimeFormat("pt-BR", { day: "numeric", month: "long", year: "numeric" }).format(b)}`;
        }
        return `${formatDate(start)} a ${formatDate(end)}`;
    }

    function slugFromUrl() {
        return new URLSearchParams(window.location.search).get("slug") || "";
    }

    async function fetchData(path) {
        const response = await fetch(path, { cache: "no-store" });
        if (!response.ok) throw new Error(`Não foi possível carregar ${path}`);
        return response.json();
    }

    async function loadCollection(folder) {
        let slugs = await fetchData(`content/${folder}/index.json`);
        try {
            const response = await fetch(`/api/github-list?path=${encodeURIComponent(`content/${folder}`)}`);
            if (response.ok) {
                const files = await response.json();
                const liveSlugs = Array.isArray(files) ? files
                    .filter((file) => file.name?.endsWith(".json") && file.name !== "index.json")
                    .map((file) => file.name.replace(/\.json$/, "")) : [];
                slugs = [...new Set([...slugs, ...liveSlugs])];
            }
        } catch (_) {
            // O índice local mantém a página funcional quando o Worker está indisponível.
        }
        const records = await Promise.all(slugs.map(async (slug) => {
            try {
                const data = await fetchData(`content/${folder}/${encodeURIComponent(slug)}.json`);
                return { ...data, slug };
            } catch (error) {
                console.warn(error);
                return null;
            }
        }));
        return records.filter(Boolean);
    }

    function statusBadge(status) {
        return `<span class="ce-status ce-status--${esc(status || "proximo")}">${esc(statusLabels[status] || status || "Atualização")}</span>`;
    }

    function setSeo(title, description, canonical) {
        document.title = `${title} | TVDUASRODAS`;
        let meta = document.querySelector('meta[name="description"]');
        if (!meta) {
            meta = document.createElement("meta");
            meta.name = "description";
            document.head.appendChild(meta);
        }
        meta.content = description || "Competições e eventos do universo das duas rodas.";
        let link = document.querySelector('link[rel="canonical"]');
        if (!link) {
            link = document.createElement("link");
            link.rel = "canonical";
            document.head.appendChild(link);
        }
        link.href = canonical;
    }

    function markdown(value) {
        const lines = String(value || "").split(/\r?\n/);
        const html = [];
        let list = false;
        const inline = (text) => esc(text)
            .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
            .replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
        for (const raw of lines) {
            const line = raw.trim();
            if (!line) { if (list) { html.push("</ul>"); list = false; } continue; }
            if (/^[-*]\s+/.test(line)) {
                if (!list) { html.push("<ul>"); list = true; }
                html.push(`<li>${inline(line.replace(/^[-*]\s+/, ""))}</li>`);
            } else {
                if (list) { html.push("</ul>"); list = false; }
                if (/^###\s+/.test(line)) html.push(`<h3>${inline(line.replace(/^###\s+/, ""))}</h3>`);
                else if (/^##\s+/.test(line)) html.push(`<h2>${inline(line.replace(/^##\s+/, ""))}</h2>`);
                else html.push(`<p>${inline(line)}</p>`);
            }
        }
        if (list) html.push("</ul>");
        return html.join("");
    }

    function competitionCard(item) {
        const next = item.next_stage || {};
        return `<article class="ce-card" data-modality="${esc((item.modality || "").toLowerCase())}">
            <a class="ce-card__media" href="competicao.html?slug=${encodeURIComponent(item.slug)}">
                <img src="${esc(safeUrl(item.cover, DEFAULT_IMAGE))}" alt="${esc(item.title)}" loading="lazy" onerror="this.src='${DEFAULT_IMAGE}'">
                ${statusBadge(item.status)}
            </a>
            <div class="ce-card__body">
                <div class="ce-eyebrow">${esc(item.modality || "Competição")} · ${esc(item.scope || item.country || "")}</div>
                <h3><a href="competicao.html?slug=${encodeURIComponent(item.slug)}">${esc(item.title)}</a></h3>
                <p>${esc(item.summary || "Resultados, calendário e classificação oficial.")}</p>
                ${next.name ? `<div class="ce-next"><span>Próxima etapa</span><strong>${esc(next.name)}</strong><small>${esc(formatRange(next.start_date, next.end_date))}${next.city ? ` · ${esc(next.city)}/${esc(next.state)}` : ""}</small></div>` : ""}
                <a class="ce-text-link" href="competicao.html?slug=${encodeURIComponent(item.slug)}">Ver resultados e classificação →</a>
            </div>
        </article>`;
    }

    function eventCard(item) {
        return `<article class="ce-event-card">
            <div class="ce-event-card__date"><strong>${esc(formatRange(item.start_date, item.end_date))}</strong><span>${esc(item.city)}, ${esc(item.state)}</span></div>
            <div class="ce-event-card__body">
                <div>${statusBadge(item.status)} ${item.free ? '<span class="ce-chip">Entrada gratuita</span>' : ""}</div>
                <h3><a href="evento.html?slug=${encodeURIComponent(item.slug)}">${esc(item.title)}</a></h3>
                <p>${esc(item.summary || "")}</p>
                <small>${esc(item.venue || "Local a confirmar")}</small>
            </div>
            <a class="ce-event-card__action" href="evento.html?slug=${encodeURIComponent(item.slug)}" aria-label="Ver detalhes de ${esc(item.title)}">→</a>
        </article>`;
    }

    async function loadLanding() {
        const competitionGrid = document.getElementById("ceCompetitionGrid");
        if (!competitionGrid) return;
        try {
            const [competitions, events] = await Promise.all([loadCollection("competitions"), loadCollection("events")]);
            competitions.sort((a, b) => Number(Boolean(b.featured)) - Number(Boolean(a.featured)) || String(a.title).localeCompare(String(b.title)));
            events.sort((a, b) => String(a.start_date).localeCompare(String(b.start_date)));
            competitionGrid.innerHTML = competitions.map(competitionCard).join("");
            document.getElementById("ceEventList").innerHTML = events.map(eventCard).join("");

            const modalities = [...new Set(competitions.map((x) => x.modality).filter(Boolean))].sort();
            const filter = document.getElementById("ceModalityFilter");
            modalities.forEach((name) => filter.insertAdjacentHTML("beforeend", `<option value="${esc(name.toLowerCase())}">${esc(name)}</option>`));
            const search = document.getElementById("ceSearch");
            const apply = () => {
                const term = search.value.toLowerCase().trim();
                const modality = filter.value;
                competitionGrid.querySelectorAll(".ce-card").forEach((card) => {
                    card.hidden = Boolean((modality && card.dataset.modality !== modality) || (term && !card.textContent.toLowerCase().includes(term)));
                });
            };
            search.addEventListener("input", apply);
            filter.addEventListener("change", apply);
        } catch (error) {
            console.error(error);
            competitionGrid.innerHTML = '<div class="ce-empty"><strong>Não foi possível carregar a central agora.</strong><p>Tente novamente em alguns instantes.</p></div>';
        }
    }

    function renderNextStage(next) {
        if (!next || !next.name) return "";
        return `<section class="ce-panel ce-next-stage"><div><span class="ce-eyebrow">Próxima etapa</span><h2>${esc(next.name)}</h2><p>${esc(formatRange(next.start_date, next.end_date))}</p></div><div><strong>${esc(next.venue || "Local a confirmar")}</strong><span>${next.city ? `${esc(next.city)}/${esc(next.state)}` : ""}</span>${next.note ? `<small>${esc(next.note)}</small>` : ""}</div></section>`;
    }

    function renderStandings(items) {
        if (!items?.length) return '<div class="ce-empty"><strong>Classificação aguardando documento oficial.</strong><p>Esta área será atualizada assim que a organização publicar os pontos.</p></div>';
        const categories = [...new Set(items.map((x) => x.category || "Geral"))];
        return categories.map((category) => {
            const rows = items.filter((x) => (x.category || "Geral") === category).sort((a, b) => a.position - b.position);
            return `<div class="ce-standing-group"><h3>${esc(category)}</h3><div class="ce-table-wrap"><table class="ce-table"><thead><tr><th>Pos.</th><th>Competidor</th><th>Equipe</th><th>Pontos</th></tr></thead><tbody>${rows.map((x) => `<tr><td><strong>${esc(x.position)}º</strong></td><td>${esc(x.competitor)}</td><td>${esc(x.team || "—")}</td><td><strong>${esc(x.points)}</strong></td></tr>`).join("")}</tbody></table></div></div>`;
        }).join("");
    }

    function renderRounds(items) {
        if (!items?.length) return '<div class="ce-empty"><strong>Calendário em confirmação.</strong><p>A programação será publicada após validação nas fontes oficiais.</p></div>';
        return `<div class="ce-table-wrap"><table class="ce-table ce-table--calendar"><thead><tr><th>Etapa</th><th>Data</th><th>Local</th><th>Resultado / situação</th></tr></thead><tbody>${items.sort((a, b) => a.order - b.order).map((x) => `<tr><td><strong>${esc(x.name)}</strong></td><td>${esc(formatRange(x.start_date, x.end_date))}</td><td>${esc(x.location)}</td><td>${x.winner ? esc(x.winner) : statusBadge(x.status)}${x.results_url ? ` <a href="${esc(safeUrl(x.results_url))}" target="_blank" rel="noopener noreferrer">Oficial ↗</a>` : ""}</td></tr>`).join("")}</tbody></table></div>`;
    }

    async function loadCompetitionDetail() {
        const root = document.getElementById("ceCompetitionDetail");
        if (!root) return;
        const slug = slugFromUrl();
        if (!/^[a-z0-9-]+$/.test(slug)) return showNotFound(root, "competição");
        try {
            const item = await fetchData(`content/competitions/${slug}.json`);
            setSeo(item.title, item.summary, `${window.location.origin}${window.location.pathname}?slug=${encodeURIComponent(slug)}`);
            const updated = item.last_updated ? new Date(item.last_updated).toLocaleString("pt-BR", { dateStyle: "long", timeStyle: "short" }) : "";
            root.innerHTML = `<header class="ce-detail-hero"><div class="ce-detail-hero__media"><img src="${esc(safeUrl(item.cover, DEFAULT_IMAGE))}" alt="${esc(item.title)}" onerror="this.src='${DEFAULT_IMAGE}'">${item.image_credit ? `<small>${esc(item.image_credit)}</small>` : ""}</div><div class="ce-detail-hero__copy">${statusBadge(item.status)}<div class="ce-eyebrow">${esc(item.modality)} · Temporada ${esc(item.season)}</div><h1>${esc(item.title)}</h1><p>${esc(item.summary)}</p><div class="ce-actions"><a class="btn btn-primary" href="${esc(safeUrl(item.official_url))}" target="_blank" rel="noopener noreferrer">Site oficial ↗</a>${item.results_url ? `<a class="btn btn-outline" href="${esc(safeUrl(item.results_url))}" target="_blank" rel="noopener noreferrer">Resultados oficiais ↗</a>` : ""}</div>${updated ? `<small class="ce-updated">Atualizado em ${esc(updated)}</small>` : ""}</div></header>${renderNextStage(item.next_stage)}<nav class="ce-anchor-nav" aria-label="Nesta página"><a href="#classificacao">Classificação</a><a href="#calendario">Etapas e resultados</a><a href="#sobre">Sobre</a></nav><section class="ce-detail-section" id="classificacao"><div class="ce-section-heading"><span class="ce-eyebrow">Leaderboard</span><h2>Classificação do campeonato</h2></div>${renderStandings(item.standings)}</section><section class="ce-detail-section" id="calendario"><div class="ce-section-heading"><span class="ce-eyebrow">Temporada ${esc(item.season)}</span><h2>Etapas e resultados</h2></div>${renderRounds(item.rounds)}</section><section class="ce-detail-section ce-prose" id="sobre">${markdown(item.body)}</section><aside class="ce-source-note"><strong>Compromisso com a precisão</strong><p>Resultados e pontos são conferidos com os documentos do organizador. Links oficiais ficam disponíveis para auditoria e podem prevalecer sobre informações provisórias.</p></aside>`;
        } catch (error) { console.error(error); showNotFound(root, "competição"); }
    }

    async function loadEventDetail() {
        const root = document.getElementById("ceEventDetail");
        if (!root) return;
        const slug = slugFromUrl();
        if (!/^[a-z0-9-]+$/.test(slug)) return showNotFound(root, "evento");
        try {
            const item = await fetchData(`content/events/${slug}.json`);
            setSeo(item.title, item.summary, `${window.location.origin}${window.location.pathname}?slug=${encodeURIComponent(slug)}`);
            root.innerHTML = `<header class="ce-detail-hero"><div class="ce-detail-hero__media"><img src="${esc(safeUrl(item.cover, DEFAULT_IMAGE))}" alt="${esc(item.title)}" onerror="this.src='${DEFAULT_IMAGE}'">${item.image_credit ? `<small>${esc(item.image_credit)}</small>` : ""}</div><div class="ce-detail-hero__copy">${statusBadge(item.status)}<div class="ce-eyebrow">${esc(item.event_type)}</div><h1>${esc(item.title)}</h1><p>${esc(item.summary)}</p><div class="ce-actions"><a class="btn btn-primary" href="${esc(safeUrl(item.official_url))}" target="_blank" rel="noopener noreferrer">Site oficial ↗</a>${item.ticket_url ? `<a class="btn btn-outline" href="${esc(safeUrl(item.ticket_url))}" target="_blank" rel="noopener noreferrer">Ingressos / acesso ↗</a>` : ""}</div></div></header><section class="ce-service-grid"><div><span>Quando</span><strong>${esc(formatRange(item.start_date, item.end_date))}</strong></div><div><span>Onde</span><strong>${esc(item.venue)}</strong><small>${esc(item.city)}/${esc(item.state)}</small></div><div><span>Acesso</span><strong>${item.free ? "Entrada gratuita" : "Consulte ingressos"}</strong></div></section><section class="ce-detail-section"><div class="ce-section-heading"><span class="ce-eyebrow">Programação</span><h2>Atrações e experiências</h2></div><div class="ce-attractions">${(item.attractions || []).map((x) => `<span>${esc(x)}</span>`).join("") || "Programação a confirmar."}</div></section><section class="ce-detail-section ce-prose">${markdown(item.body)}</section><aside class="ce-source-note"><strong>Antes de sair de casa</strong><p>Horários, atrações e regras podem mudar. Confirme as informações no site oficial do evento.</p></aside>`;
        } catch (error) { console.error(error); showNotFound(root, "evento"); }
    }

    function showNotFound(root, type) {
        root.innerHTML = `<div class="ce-empty ce-empty--large"><h1>${type === "evento" ? "Evento" : "Competição"} não encontrado</h1><p>O endereço pode ter mudado ou o conteúdo ainda está em preparação.</p><a class="btn btn-primary" href="competicoes-eventos.html">Voltar à central</a></div>`;
    }

    document.addEventListener("DOMContentLoaded", () => {
        loadLanding();
        loadCompetitionDetail();
        loadEventDetail();
    });
})();
