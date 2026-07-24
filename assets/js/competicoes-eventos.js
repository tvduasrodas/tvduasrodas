(function () {
    "use strict";

    const DEFAULT_IMAGE = "/assets/img/competicoes-eventos-default.svg";
    const LIST_LIMIT = 8;
    const HIGHLIGHT_SLUGS = [
        "arena-cross-brasil-2026",
        "moto1000gp-2026",
        "motogp-2026",
        "brasileiro-motocross-2026",
        "superbike-brasil-2026",
        "sertoes-2026",
        "brasileiro-ciclismo-mtb-2026",
        "worldsbk-2026"
    ];
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

    function slugify(value) {
        return String(value || "")
            .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
            .toLowerCase().replace(/[^a-z0-9]+/g, "-")
            .replace(/^-+|-+$/g, "");
    }

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

    function calendarItem(item) {
        const location = [item.city, item.state].filter(Boolean).join("/") || item.location || "Local a confirmar";
        const calendarSlug = slugify(`${item.title}-${item.start_date || ""}`);
        const detail = item.competition_slug
            ? `competicao.html?slug=${encodeURIComponent(item.competition_slug)}`
            : `evento.html?slug=${encodeURIComponent(calendarSlug)}`;
        return `<article class="ce-calendar-item" data-modality="${esc((item.modality || "").toLowerCase())}">
            <div class="ce-calendar-item__date"><strong>${esc(formatRange(item.start_date, item.end_date))}</strong><span>${esc(location)}</span></div>
            <div class="ce-calendar-item__body"><small>${esc(item.modality || "Duas rodas")}</small><h3>${esc(item.title)}</h3><p>${esc(item.stage || "Programação oficial")}${item.note ? ` · ${esc(item.note)}` : ""}</p></div>
            <a href="${esc(detail)}" aria-label="Ver ${esc(item.title)}">Ver detalhes →</a>
        </article>`;
    }

    function setupSearchablePicker(input, select, button, records) {
        if (!input || !select || !button) return;
        const allOptions = records.slice().sort((a, b) => String(a.label).localeCompare(String(b.label), "pt-BR"));
        const render = (query = "") => {
            const normalized = query.trim().toLocaleLowerCase("pt-BR");
            const filtered = allOptions.filter((item) => !normalized || item.search.includes(normalized));
            select.innerHTML = `<option value="">${filtered.length ? "Selecione na lista" : "Nenhum resultado"}</option>` +
                filtered.map((item) => `<option value="${esc(item.value)}" data-kind="${esc(item.kind)}">${esc(item.label)}</option>`).join("");
            select.disabled = !filtered.length;
            button.disabled = true;
        };
        const openSelected = () => {
            const option = select.selectedOptions[0];
            if (!option?.value) return;
            window.location.href = `${option.dataset.kind === "competition" ? "competicao" : "evento"}.html?slug=${encodeURIComponent(option.value)}`;
        };
        input.addEventListener("input", () => render(input.value));
        select.addEventListener("change", () => {
            button.disabled = !select.value;
            if (select.value) input.value = select.selectedOptions[0].textContent;
        });
        input.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                const first = [...select.options].find((option) => option.value);
                if (first) {
                    select.value = first.value;
                    button.disabled = false;
                    openSelected();
                }
            }
        });
        button.addEventListener("click", openSelected);
        render();
    }

    function adRectangle() {
        return `<aside class="site-ad-rectangle" aria-label="Espaço publicitário"><a href="contato.html#patrocinio"><span>Publicidade</span><strong>Sua marca em movimento.</strong><small>Anuncie para quem vive o universo das duas rodas</small><em>Conheça os formatos →</em></a></aside>`;
    }

    async function loadLanding() {
        const competitionGrid = document.getElementById("ceCompetitionGrid");
        if (!competitionGrid) return;
        try {
            const [competitions, events, calendar] = await Promise.all([
                loadCollection("competitions"),
                loadCollection("events"),
                fetchData("content/calendar/cbm-2026.json").catch(() => ({ entries: [] }))
            ]);
            competitions.sort((a, b) => Number(Boolean(b.featured)) - Number(Boolean(a.featured)) || String(a.title).localeCompare(String(b.title)));
            events.sort((a, b) => String(a.start_date).localeCompare(String(b.start_date)));
            const highlights = HIGHLIGHT_SLUGS.map((slug) => competitions.find((item) => item.slug === slug)).filter(Boolean);
            competitionGrid.innerHTML = highlights.slice(0, LIST_LIMIT).map(competitionCard).join("");

            const calendarEntries = Array.isArray(calendar.entries) ? calendar.entries
                .sort((a, b) => String(a.start_date).localeCompare(String(b.start_date))) : [];
            const competitionPickerRecords = [
                ...competitions.map((item) => ({
                    value: item.slug,
                    kind: "competition",
                    label: item.title,
                    search: [item.title, item.modality, item.scope, item.country].filter(Boolean).join(" ").toLocaleLowerCase("pt-BR")
                })),
                ...calendarEntries.filter((item) => !item.competition_slug).map((item) => ({
                    value: slugify(`${item.title}-${item.start_date || ""}`),
                    kind: "event",
                    label: `${item.title} — ${formatDate(item.start_date)}`,
                    search: [item.title, item.modality, item.stage, item.city, item.state].filter(Boolean).join(" ").toLocaleLowerCase("pt-BR")
                }))
            ];
            setupSearchablePicker(
                document.getElementById("ceCompetitionSearch"),
                document.getElementById("ceCompetitionSelect"),
                document.getElementById("ceCompetitionOpen"),
                competitionPickerRecords
            );
            const calendarList = document.getElementById("ceCalendarList");
            const calendarFilter = document.getElementById("ceCalendarFilter");
            [...new Set(calendarEntries.map((x) => x.modality).filter(Boolean))].sort()
                .forEach((name) => calendarFilter.insertAdjacentHTML("beforeend", `<option value="${esc(name.toLowerCase())}">${esc(name)}</option>`));

            let calendarExpanded = false;
            const calendarMore = document.getElementById("ceCalendarMore");
            const renderCalendar = () => {
                const filtered = calendarEntries.filter((item) => !calendarFilter.value || (item.modality || "").toLowerCase() === calendarFilter.value);
                const shown = calendarExpanded ? filtered : filtered.slice(0, LIST_LIMIT);
                calendarList.innerHTML = shown.length ? shown.map(calendarItem).join("") : '<div class="ce-empty"><strong>Nenhuma data nesta modalidade.</strong><p>Escolha outro filtro.</p></div>';
                calendarMore.hidden = filtered.length <= LIST_LIMIT;
                calendarMore.textContent = calendarExpanded ? "Mostrar somente os próximos 8" : `Mostrar agenda completa (${filtered.length})`;
            };
            calendarFilter.addEventListener("change", () => {
                calendarExpanded = false;
                renderCalendar();
            });
            calendarMore.addEventListener("click", () => { calendarExpanded = !calendarExpanded; renderCalendar(); });
            renderCalendar();

            const eventList = document.getElementById("ceEventList");
            const eventMore = document.getElementById("ceEventMore");
            let eventsExpanded = false;
            const renderEvents = () => {
                eventList.innerHTML = (eventsExpanded ? events : events.slice(0, LIST_LIMIT)).map(eventCard).join("");
                eventMore.hidden = events.length <= LIST_LIMIT;
                eventMore.textContent = eventsExpanded ? "Mostrar somente os próximos 8" : `Mostrar todos os eventos (${events.length})`;
            };
            eventMore.addEventListener("click", () => { eventsExpanded = !eventsExpanded; renderEvents(); });
            renderEvents();

            setupSearchablePicker(
                document.getElementById("ceEventSearch"),
                document.getElementById("ceEventSelect"),
                document.getElementById("ceEventOpen"),
                events.map((item) => ({
                    value: item.slug,
                    kind: "event",
                    label: `${item.title} — ${formatDate(item.start_date)}`,
                    search: [item.title, item.event_type, item.city, item.state, item.summary].filter(Boolean).join(" ").toLocaleLowerCase("pt-BR")
                }))
            );
        } catch (error) {
            console.error(error);
            competitionGrid.innerHTML = '<div class="ce-empty"><strong>Não foi possível carregar a central agora.</strong><p>Tente novamente em alguns instantes.</p></div>';
        }
    }

    function renderNextStage(next) {
        if (!next || !next.name) return "";
        return `<section class="ce-panel ce-next-stage"><div><span class="ce-eyebrow">Próxima etapa</span><h2>${esc(next.name)}</h2><p>${esc(formatRange(next.start_date, next.end_date))}</p></div><div><strong>${esc(next.venue || "Local a confirmar")}</strong><span>${next.city ? `${esc(next.city)}/${esc(next.state)}` : ""}</span>${next.note ? `<small>${esc(next.note)}</small>` : ""}</div></section>`;
    }

    function renderStandings(items, valueLabel = "Pontos") {
        if (!items?.length) return '<div class="ce-empty"><strong>Classificação aguardando documento oficial.</strong><p>Esta área será atualizada assim que a organização publicar os pontos.</p></div>';
        const categories = [...new Set(items.map((x) => x.category || "Geral"))];
        return categories.map((category) => {
            const rows = items.filter((x) => (x.category || "Geral") === category).sort((a, b) => a.position - b.position);
            return `<div class="ce-standing-group"><h3>${esc(category)}</h3><div class="ce-table-wrap"><table class="ce-table"><thead><tr><th>Pos.</th><th>Competidor</th><th>Equipe</th><th>${esc(valueLabel)}</th></tr></thead><tbody>${rows.map((x) => `<tr><td><strong>${esc(x.position)}º</strong></td><td>${esc(x.competitor)}</td><td>${esc(x.team || "—")}</td><td><strong>${esc(x.points ?? "—")}</strong></td></tr>`).join("")}</tbody></table></div></div>`;
        }).join("");
    }

    function renderLatestResult(result) {
        if (!result?.classification?.length) return "";
        const rows = result.classification.map((x) => `<tr><td><strong>${esc(x.position)}</strong></td><td>${esc(x.competitor)}</td><td>${esc(x.team || "—")}</td><td>${esc(x.time_gap || "—")}</td><td><strong>${esc(x.points ?? "—")}</strong></td></tr>`).join("");
        return `<section class="ce-detail-section" id="resultado-recente"><div class="ce-section-heading"><span class="ce-eyebrow">Resultado oficial mais recente</span><h2>${esc(result.event)}</h2>${result.session || result.date ? `<p>${esc([result.session, result.date ? formatDate(result.date, { long: true }) : ""].filter(Boolean).join(" · "))}</p>` : ""}</div>${result.note ? `<p>${esc(result.note)}</p>` : ""}<div class="ce-table-wrap"><table class="ce-table"><thead><tr><th>Pos.</th><th>Piloto</th><th>Equipe</th><th>Tempo / diferença</th><th>Pontos</th></tr></thead><tbody>${rows}</tbody></table></div>${result.source_url ? `<p><a href="${esc(safeUrl(result.source_url))}" target="_blank" rel="noopener noreferrer">Conferir classificação oficial completa ↗</a></p>` : ""}</section>`;
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
            const latestResult = renderLatestResult(item.latest_result);
            root.innerHTML = `<header class="ce-detail-hero"><div class="ce-detail-hero__media"><img src="${esc(safeUrl(item.cover, DEFAULT_IMAGE))}" alt="${esc(item.title)}" onerror="this.src='${DEFAULT_IMAGE}'">${item.image_credit ? `<small>${esc(item.image_credit)}</small>` : ""}</div><div class="ce-detail-hero__copy">${statusBadge(item.status)}<div class="ce-eyebrow">${esc(item.modality)} · Temporada ${esc(item.season)}</div><h1>${esc(item.title)}</h1><p>${esc(item.summary)}</p><div class="ce-actions"><a class="btn btn-primary" href="${esc(safeUrl(item.official_url))}" target="_blank" rel="noopener noreferrer">Site oficial ↗</a>${item.results_url ? `<a class="btn btn-outline" href="${esc(safeUrl(item.results_url))}" target="_blank" rel="noopener noreferrer">Resultados oficiais ↗</a>` : ""}</div>${updated ? `<small class="ce-updated">Atualizado em ${esc(updated)}</small>` : ""}</div></header>${adRectangle()}${renderNextStage(item.next_stage)}<nav class="ce-anchor-nav" aria-label="Nesta página">${latestResult ? '<a href="#resultado-recente">Último resultado</a>' : ""}<a href="#classificacao">Classificação</a><a href="#calendario">Etapas e resultados</a><a href="#sobre">Sobre</a></nav>${latestResult}<section class="ce-detail-section" id="classificacao"><div class="ce-section-heading"><span class="ce-eyebrow">${esc(item.standings_eyebrow || "Leaderboard")}</span><h2>${esc(item.standings_title || "Classificação do campeonato")}</h2></div>${renderStandings(item.standings, item.standings_value_label || "Pontos")}</section><section class="ce-detail-section" id="calendario"><div class="ce-section-heading"><span class="ce-eyebrow">Temporada ${esc(item.season)}</span><h2>Etapas e resultados</h2></div>${renderRounds(item.rounds)}</section><section class="ce-detail-section ce-prose" id="sobre">${markdown(item.body)}</section><aside class="ce-source-note"><strong>Compromisso com a precisão</strong><p>Resultados e pontos são conferidos com documentos da entidade, do organizador ou de prestadores oficialmente contratados, com verificação cruzada em outras fontes confiáveis quando necessário.</p></aside>`;
        } catch (error) { console.error(error); showNotFound(root, "competição"); }
    }

    async function loadEventDetail() {
        const root = document.getElementById("ceEventDetail");
        if (!root) return;
        const slug = slugFromUrl();
        if (!/^[a-z0-9-]+$/.test(slug)) return showNotFound(root, "evento");
        try {
            let item;
            try {
                item = await fetchData(`content/events/${slug}.json`);
            } catch (_) {
                const calendar = await fetchData("content/calendar/cbm-2026.json");
                const entry = (calendar.entries || []).find((candidate) =>
                    !candidate.competition_slug &&
                    slugify(`${candidate.title}-${candidate.start_date || ""}`) === slug
                );
                if (!entry) throw _;
                item = {
                    ...entry,
                    event_type: entry.modality || "Competição e evento",
                    venue: entry.location || [entry.city, entry.state].filter(Boolean).join("/") || "Local a confirmar",
                    cover: DEFAULT_IMAGE,
                    image_credit: "Arte: TVDUASRODAS",
                    free: false,
                    summary: [entry.stage, entry.city, entry.state].filter(Boolean).join(" · "),
                    attractions: [entry.stage || "Programação oficial"],
                    body: `## Sobre a prova\n\n${entry.title} integra o calendário monitorado pela TVDUASRODAS. A página será atualizada com programação, resultados e classificação conforme a publicação por entidades, organizadores ou prestadores oficiais.\n\n## Fonte\n\nConsulte a programação e eventuais alterações no canal oficial indicado nesta página.`
                };
            }
            setSeo(item.title, item.summary, `${window.location.origin}${window.location.pathname}?slug=${encodeURIComponent(slug)}`);
            root.innerHTML = `<header class="ce-detail-hero"><div class="ce-detail-hero__media"><img src="${esc(safeUrl(item.cover, DEFAULT_IMAGE))}" alt="${esc(item.title)}" onerror="this.src='${DEFAULT_IMAGE}'">${item.image_credit ? `<small>${esc(item.image_credit)}</small>` : ""}</div><div class="ce-detail-hero__copy">${statusBadge(item.status)}<div class="ce-eyebrow">${esc(item.event_type)}</div><h1>${esc(item.title)}</h1><p>${esc(item.summary)}</p><div class="ce-actions"><a class="btn btn-primary" href="${esc(safeUrl(item.official_url))}" target="_blank" rel="noopener noreferrer">Site oficial ↗</a>${item.ticket_url ? `<a class="btn btn-outline" href="${esc(safeUrl(item.ticket_url))}" target="_blank" rel="noopener noreferrer">Ingressos / acesso ↗</a>` : ""}</div></div></header>${adRectangle()}<section class="ce-service-grid"><div><span>Quando</span><strong>${esc(formatRange(item.start_date, item.end_date))}</strong></div><div><span>Onde</span><strong>${esc(item.venue)}</strong><small>${esc([item.city, item.state].filter(Boolean).join("/"))}</small></div><div><span>Acesso</span><strong>${item.free ? "Entrada gratuita" : "Consulte o site oficial"}</strong></div></section><section class="ce-detail-section"><div class="ce-section-heading"><span class="ce-eyebrow">Programação</span><h2>Atrações e experiências</h2></div><div class="ce-attractions">${(item.attractions || []).map((x) => `<span>${esc(x)}</span>`).join("") || "Programação a confirmar."}</div></section><section class="ce-detail-section ce-prose">${markdown(item.body)}</section><aside class="ce-source-note"><strong>Antes de sair de casa</strong><p>Horários, atrações e regras podem mudar. Confirme as informações no site oficial do evento.</p></aside>`;
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
