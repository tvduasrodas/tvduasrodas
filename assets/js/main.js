// ============================
// CONFIG PARA LISTAR MATÉRIAS (HOME) VIA GITHUB
// ============================
const GITHUB_OWNER = "tvduasrodas";      // ajuste se o repositório for outro
const GITHUB_REPO = "tvduasrodas/tvduasrodas";       // idem
const GITHUB_BRANCH = "main";
const ARTICLES_PATH = "content/articles";
const GITHUB_ARTICLES_API_URL =
    `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${ARTICLES_PATH}?ref=${GITHUB_BRANCH}`;

// Data no formato "23 jan 2026" → Date
function parseArticleDate(dateStr) {
    if (!dateStr) return new Date(0);
    const direct = new Date(dateStr);
    if (!isNaN(direct.getTime())) return direct;

    const parts = dateStr.toLowerCase().trim().split(/\s+/);
    if (parts.length < 3) return new Date(0);
    const day = parseInt(parts[0], 10);
    const monthStr = parts[1].slice(0, 3);
    const year = parseInt(parts[2], 10);

    const months = {
        jan: 0, fev: 1, mar: 2, abr: 3, mai: 4, jun: 5,
        jul: 6, ago: 7, set: 8, out: 9, nov: 10, dez: 11
    };

    const month = months[monthStr];
    if (isNaN(day) || isNaN(year) || month === undefined) {
        return new Date(0);
    }
    return new Date(year, month, day);
}


document.addEventListener("DOMContentLoaded", () => {

    /* ============================
   ÍNDICE ESTÁTICO DE CONTEÚDOS PARA BUSCA
   ============================ */
    const SITE_INDEX = [
        // Exemplos – você pode ir aumentando essa lista

        // Matérias da revista (revista.html)

        {
            title: "Naked urbana 300cc: uso real na cidade",
            description: "Review completa da naked 300cc no trânsito urbano e em pequenos rolês.",
            type: "materia",
            category: "motos",
            url: "materia.html?slug=review-naked-300",
        },


        {
            title: "Scooters elétricas na cidade: vale a pena?",
            description: "Guia completo sobre consumo, autonomia, recarga e manutenção de scooters elétricas.",
            type: "materia",
            category: "eletrico",
            url: "guia-scooters-eletricas.html",
        },
        {
            title: "Viagem de serra: mirantes, curvas e segurança",
            description: "Dicas de roteiro, equipamento e pilotagem para aproveitar a serra com segurança.",
            type: "materia",
            category: "viagem",
            url: "viagem-serra-mirantes.html",
        },
        {
            title: "Rolê urbano noturno: luzes da cidade em duas rodas",
            description: "Como curtir o rolê noturno com segurança e boa visibilidade.",
            type: "materia",
            category: "urbano",
            url: "role-urbano-noturno.html",
        },

        // Vídeos da TV (tv.html – galeria)
        {
            title: "Cassetadas · Episódio 01",
            description: "Quedas, erros e situações inusitadas em duas rodas.",
            type: "video_tv",
            category: "cassetadas",
            videoId: "xcPxjtQU1qc", 
            url: "tv.html?v=xcPxjtQU1qc",
        },
        {
            title: "Cassetadas · Episódio 02",
            description: "Mais momentos engraçados e imprevistos.",
            type: "video_tv",
            category: "cassetadas",
            videoId: "3GwjfUFyY6M",
            url: "tv.html?v=3GwjfUFyY6M",
        },
        {
            title: "Cross · Treino na pista",
            description: "Saltos, curvas e técnica em pista de terra.",
            type: "video_tv",
            category: "cross",
            videoId: "2vjPBrBU-TM",
            url: "tv.html?v=2vjPBrBU-TM",
        },
        {
            title: "Cross · Corrida completa",
            description: "Prova com vários pilotos e muita adrenalina.",
            type: "video_tv",
            category: "cross",
            videoId: "L_jWHffIx5E",
            url: "tv.html?v=L_jWHffIx5E",
        },
        {
            title: "Rolê urbano · Night ride",
            description: "Rolê noturno passando pelos principais pontos da cidade.",
            type: "video_tv",
            category: "urbano",
            videoId: "kXYiU_JCYtU",
            url: "tv.html?v=kXYiU_JCYtU",
        },
        {
            title: "Viagem · Serra e mirantes",
            description: "Subida de serra com paradas em mirantes e visual incrível.",
            type: "video_tv",
            category: "viagem",
            videoId: "hTWKbfoikeg",
            url: "tv.html?v=hTWKbfoikeg",
        },

        // Vídeos em destaque na home (index.html)
        {
            title: "Live · TV Duas Rodas",
            description: "Transmissão ao vivo com chat, convidados e novidades.",
            type: "video_home",
            category: "live",
            videoId: "xcPxjtQU1qc",
            url: "tv.html?v=xcPxjtQU1qc",
        },
        {
            title: "Rolê de Rua · Episódio 01",
            description: "Night ride pela cidade com foco na experiência de pilotagem.",
            type: "video_home",
            category: "urbano",
            videoId: "3GwjfUFyY6M",
            url: "tv.html?v=3GwjfUFyY6M",
        },
    ];


    /* ============================
       FILTRO DE MATÉRIAS (REVISTA)
       ============================ */
    const filterButtons = document.querySelectorAll(".filter-btn");
    const articleGrid = document.getElementById("articleGrid");

    if (filterButtons.length && articleGrid) {
        const cards = articleGrid.querySelectorAll(".article-card");

        filterButtons.forEach((btn) => {
            btn.addEventListener("click", () => {
                const filter = btn.getAttribute("data-filter");

                filterButtons.forEach((b) => b.classList.remove("active"));
                btn.classList.add("active");

                cards.forEach((card) => {
                    const category = card.getAttribute("data-category");
                    if (filter === "all" || filter === category) {
                        card.style.display = "";
                    } else {
                        card.style.display = "none";
                    }
                });
            });
        });
    }

    /* ============================
       SIMULAÇÃO LIVE ON/OFF (HOME / TV)
       ============================ */
    const liveToggleBtn = document.querySelector("[data-toggle-live]");
    if (liveToggleBtn) {
        const liveStatus = document.querySelector(".live-status");
        const statusDot = document.querySelector(".status-dot");

        liveToggleBtn.addEventListener("click", () => {
            if (!liveStatus || !statusDot) return;

            const isOff = liveStatus.classList.contains("live-status-off");

            if (isOff) {
                liveStatus.textContent = "Ao vivo";
                liveStatus.classList.remove("live-status-off");
                liveStatus.classList.add("live-status-on");

                statusDot.textContent = "live";
                statusDot.classList.remove("status-off");
                statusDot.classList.add("status-on");
            } else {
                liveStatus.textContent = "Offline";
                liveStatus.classList.remove("live-status-on");
                liveStatus.classList.add("live-status-off");

                statusDot.textContent = "off-air";
                statusDot.classList.remove("status-on");
                statusDot.classList.add("status-off");
            }
        });
    }

    /* ============================
       FUNÇÕES YOUTUBE – NORMALIZAR ID
       ============================ */
    function normalizeYouTubeId(value) {
        if (!value) return null;

        // Se for URL
        if (value.includes("youtube.com") || value.includes("youtu.be")) {
            try {
                const url = new URL(value);

                // youtu.be/ID
                if (url.hostname.includes("youtu.be")) {
                    return url.pathname.replace("/", "");
                }

                // youtube.com/watch?v=ID
                const v = url.searchParams.get("v");
                if (v) return v;
            } catch (e) {
                // ignora erro e cai no return final
            }
        }

        // Se não for URL, assume que já é ID
        return value;
    }

    /* ============================
       TV PAGE – PLAYER + GALERIA
       ============================ */
    const mainPlayer = document.getElementById("mainPlayer");
    const tvGallery = document.getElementById("tvGallery");
    const tvCards = tvGallery ? tvGallery.querySelectorAll(".tv-video-card") : [];
    const defaultVideoId = mainPlayer ? mainPlayer.dataset.defaultId : null;
    const mainTitleEl = document.getElementById("tvMainTitle");
    const mainDescEl = document.getElementById("tvMainDescription");


    function setMainVideo(videoId) {
        if (!mainPlayer) return;

        const finalId = normalizeYouTubeId(videoId || defaultVideoId);
        if (!finalId) return;

        const baseSrc = "https://www.youtube.com/embed/";
        mainPlayer.src = baseSrc + finalId;

        let currentCard = null;

        // Marca card ativo e encontra o card atual
        tvCards.forEach((card) => {
            const cardId = normalizeYouTubeId(card.getAttribute("data-video-id"));
            const isActive = cardId === finalId;
            card.classList.toggle("active", isActive);
            if (isActive) currentCard = card;
        });

        // Atualiza título e descrição do vídeo atual
        if (currentCard && mainTitleEl && mainDescEl) {
            const titleEl = currentCard.querySelector("h3");
            const descEl = currentCard.querySelector("p");

            if (titleEl) mainTitleEl.textContent = titleEl.textContent;
            if (descEl) mainDescEl.textContent = descEl.textContent;
        }
    }


    // Lê ?v= da URL na página tv.html
    if (mainPlayer) {
        const params = new URLSearchParams(window.location.search);
        const urlVideoId = params.get("v");
        if (urlVideoId) {
            setMainVideo(urlVideoId);
        } else {
            setMainVideo(defaultVideoId);
        }
    }

    // Clique nos cards da TV para trocar o vídeo principal
    if (tvCards.length && mainPlayer) {
        tvCards.forEach((card) => {
            card.addEventListener("click", () => {
                const vid = card.getAttribute("data-video-id");
                setMainVideo(vid);

                // Em telas pequenas, rola a página até o player
                if (window.innerWidth < 900) {
                    mainPlayer.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            });
        });
    }

    /* ============================
       TV – FILTRO + PAGINAÇÃO DA GALERIA
       ============================ */
    const tvFilterButtons = document.querySelectorAll(".tv-filter-btn");
    const paginationTop = document.getElementById("tvPaginationTop");
    const paginationBottom = document.getElementById("tvPaginationBottom");

    let tvCurrentPage = 1;
    const tvPerPage = 6;
    let tvCurrentFilter = "all";

    function getFilteredCards() {
        const cards = Array.from(tvCards);
        if (tvCurrentFilter === "all") return cards;
        return cards.filter(
            (card) =>
                card.getAttribute("data-category") === tvCurrentFilter
        );
    }

    function renderTvPagination(totalPages) {
        if (!paginationTop && !paginationBottom) return;

        const containers = [paginationTop, paginationBottom].filter(Boolean);

        containers.forEach((container) => {
            container.innerHTML = "";

            for (let i = 1; i <= totalPages; i++) {
                const btn = document.createElement("button");
                btn.type = "button";
                btn.className = "tv-page-btn" + (i === tvCurrentPage ? " active" : "");
                btn.textContent = i;
                btn.dataset.page = i;

                btn.addEventListener("click", () => {
                    tvCurrentPage = i;
                    renderTvGallery();
                });

                container.appendChild(btn);
            }
        });
    }

    function renderTvGallery() {
        if (!tvGallery || !tvCards.length) return;

        const filtered = getFilteredCards();
        const totalPages = Math.max(
            1,
            Math.ceil(filtered.length / tvPerPage)
        );

        if (tvCurrentPage > totalPages) tvCurrentPage = totalPages;

        const start = (tvCurrentPage - 1) * tvPerPage;
        const end = start + tvPerPage;

        // Esconde tudo
        tvCards.forEach((card) => {
            card.style.display = "none";
        });

        // Mostra apenas o que cabe na página atual
        filtered.slice(start, end).forEach((card) => {
            card.style.display = "";
        });

        renderTvPagination(totalPages);
    }

    // Eventos dos botões de filtro na TV
    if (tvFilterButtons.length && tvCards.length) {
        tvFilterButtons.forEach((btn) => {
            btn.addEventListener("click", () => {
                const filter = btn.getAttribute("data-filter");
                tvCurrentFilter = filter;
                tvCurrentPage = 1;

                tvFilterButtons.forEach((b) => b.classList.remove("active"));
                btn.classList.add("active");

                renderTvGallery();
            });
        });

        // Render inicial
        renderTvGallery();
    }

    /* ============================
    PÁGINA DE RESULTADOS DE BUSCA (busca.html)
    ============================ */
    const searchResultsContainer = document.getElementById("searchResults");
    const searchSummary = document.getElementById("searchSummary");
    const headerSearchInput = document.getElementById("siteSearchInput");
    const headerSearchClear = document.getElementById("siteSearchClear");

    // Se estou na página busca.html
    if (searchResultsContainer && searchSummary) {
        const params = new URLSearchParams(window.location.search);
        const termRaw = params.get("q") || "";
        const term = termRaw.trim().toLowerCase();

        // Preenche o campo de busca no header com o termo atual
        if (headerSearchInput) {
            headerSearchInput.value = termRaw;
        }

        // Configura o botão "x" de limpar
        if (headerSearchClear && headerSearchInput) {
            headerSearchClear.style.display = termRaw ? "block" : "none";
            headerSearchClear.addEventListener("click", () => {
                headerSearchInput.value = "";
                window.location.href = "busca.html"; // volta pra busca "vazia"
            });
        }

        if (!term) {
            searchSummary.textContent =
                "Digite um termo na barra de busca acima para encontrar matérias, vídeos e conteúdos da TV Duas Rodas.";
            searchResultsContainer.innerHTML = "";
        } else {
            // Filtra o índice
            const results = SITE_INDEX.filter((item) => {
                const haystack =
                    (item.title + " " + item.description + " " + (item.category || "")).toLowerCase();
                return haystack.includes(term);
            });

            if (!results.length) {
                searchSummary.textContent = `Nenhum resultado encontrado para “${termRaw}”.`;
                searchResultsContainer.innerHTML = "";
            } else {
                searchSummary.textContent = `Encontrados ${results.length} resultado(s) para “${termRaw}”.`;

                searchResultsContainer.innerHTML = results
                    .map((item) => {
                        const isVideo =
                            item.type === "video_tv" || item.type === "video_home";

                        const typeLabel = isVideo ? "Vídeo" : "Matéria";

                        // Se for vídeo e tiver videoId, monta a URL do thumb
                        const thumbStyle =
                            isVideo && item.videoId
                                ? `style="background-image:url('https://img.youtube.com/vi/${item.videoId}/hqdefault.jpg');background-size:cover;background-position:center;"`
                                : "";

                        return `
          <article class="card article-card ${isVideo ? "search-video-card" : ""
                            }">
            <span class="category-tag">
              ${typeLabel}${item.category ? " · " + item.category : ""}
            </span>

            ${isVideo
                                ? `<div class="search-video-thumb" ${thumbStyle}>
                     <span class="search-play-icon"></span>
                   </div>`
                                : ""
                            }

            <h3>${item.title}</h3>
            <p>${item.description}</p>
            <a href="${item.url}" class="article-link">
              ${isVideo ? "Assistir vídeo" : "Ler matéria"} &rarr;
            </a>
          </article>
        `;
                    })
                    .join("");

            }
        }
    } else {
        // Não estou em busca.html, mas ainda quero que o botão "x" limpe o input
        if (headerSearchInput && headerSearchClear) {
            headerSearchClear.style.display = headerSearchInput.value ? "block" : "none";

            headerSearchClear.addEventListener("click", () => {
                headerSearchInput.value = "";
                headerSearchClear.style.display = "none";
                headerSearchInput.focus();
            });
        }
    }

    /* ============================
   CARREGAMENTO DE MATÉRIA DINÂMICA (materia.html?slug=...)
   ============================ */

    const articleMain = document.getElementById("articleMain");

    if (articleMain) {
        const params = new URLSearchParams(window.location.search);
        const slug = params.get("slug");

        if (!slug) {
            document.getElementById("articleTitle").textContent = "Matéria não encontrada";
            document.getElementById("articleBody").innerHTML =
                "<p>Slug não informado na URL. Use <code>?slug=...</code>.</p>";
        } else {
            fetch(`content/articles/${slug}.json`)
                .then((res) => {
                    if (!res.ok) {
                        throw new Error("Não encontrado");
                    }
                    return res.json();
                })
                .then((data) => {
                    // Título da aba
                    document.title = `${data.title} | TV Duas Rodas`;

                    // Cabeçalho
                    const tag = document.getElementById("articleTag");
                    const titleEl = document.getElementById("articleTitle");
                    const bcTag = document.getElementById("articleBreadcrumbTag");
                    const authorEl = document.getElementById("articleAuthor");
                    const dateEl = document.getElementById("articleDate");
                    const readEl = document.getElementById("articleReadingTime");

                    if (tag) tag.textContent = data.tagline || data.category || "Matéria";
                    if (bcTag) bcTag.textContent = data.kicker || data.category || "Matéria";
                    if (titleEl) titleEl.textContent = data.title || "";
                    if (authorEl) authorEl.textContent = data.author
                        ? `Por ${data.author}`
                        : "Por Redação TV Duas Rodas";
                    if (dateEl) dateEl.textContent = data.date || "";
                    if (readEl) readEl.textContent = data.readingTime
                        ? `Leitura: ${data.readingTime}`
                        : "";

                    // Patrocínio
                    const sponsorWrapper = document.getElementById("articleSponsorWrapper");
                    const sponsorEl = document.getElementById("articleSponsor");
                    if (data.sponsor && sponsorWrapper && sponsorEl) {
                        sponsorWrapper.hidden = false;
                        sponsorEl.textContent = data.sponsor;
                    }

                    // HERO: vídeo ou imagem
                    const hero = data.hero || {};
                    const heroVideoWrapper = document.getElementById("articleHeroVideo");
                    const heroIframe = document.getElementById("articleHeroIframe");
                    const heroImageWrapper = document.getElementById("articleHeroImage");
                    const heroImageTag = document.getElementById("articleHeroImageTag");
                    const heroCaption = document.getElementById("articleHeroCaption");

                    if (data.videoId && heroVideoWrapper && heroIframe) {
                        heroVideoWrapper.hidden = false;
                        heroIframe.src = `https://www.youtube.com/embed/${data.videoId}`;
                        heroIframe.title = data.title || "Vídeo da matéria";

                        // Botão "Assistir na TV & Vídeos"
                        const ctaContainer = document.getElementById("articleVideoCtaContainer");
                        if (ctaContainer) {
                            ctaContainer.innerHTML = `
              <div class="article-video-cta">
                <a href="tv.html?v=${data.videoId}" class="btn btn-outline btn-small">
                  Assistir na TV &amp; Vídeos &rarr;
                </a>
              </div>
            `;
                        }
                    } else if (heroImageWrapper && heroImageTag) {
                        heroImageWrapper.hidden = false;
                        heroImageTag.src = hero.image || "";
                        heroImageTag.alt = hero.alt || data.title || "";
                        if (heroCaption) {
                            heroCaption.textContent = hero.caption || "";
                        }
                    }

                    // Corpo da matéria
                    const bodyEl = document.getElementById("articleBody");
                    if (bodyEl && data.bodyHtml) {
                        bodyEl.innerHTML = data.bodyHtml;
                    }

                    // Compartilhamento
                    const shareBaseUrl = `${window.location.origin}${window.location.pathname}?slug=${encodeURIComponent(
                        data.slug || slug
                    )}`;
                    const shareFb = document.getElementById("shareFb");
                    const shareTw = document.getElementById("shareTw");
                    const shareWa = document.getElementById("shareWa");

                    if (shareFb) {
                        shareFb.href = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(
                            shareBaseUrl
                        )}`;
                    }
                    if (shareTw) {
                        shareTw.href = `https://twitter.com/intent/tweet?url=${encodeURIComponent(
                            shareBaseUrl
                        )}&text=${encodeURIComponent(data.title || "")}`;
                    }
                    if (shareWa) {
                        shareWa.href = `https://api.whatsapp.com/send?text=${encodeURIComponent(
                            `${data.title || "Matéria"} - ${shareBaseUrl}`
                        )}`;
                    }
                })
                .catch(() => {
                    const titleEl = document.getElementById("articleTitle");
                    const bodyEl = document.getElementById("articleBody");
                    if (titleEl) titleEl.textContent = "Matéria não encontrada";
                    if (bodyEl) {
                        bodyEl.innerHTML =
                            "<p>Não encontramos a matéria para este endereço. Verifique o link ou volte para a <a href='revista.html'>Revista</a>.</p>";
                    }
                });
        }
    }



});
