document.addEventListener("DOMContentLoaded", () => {

    /* ============================
   ÍNDICE ESTÁTICO DE CONTEÚDOS PARA BUSCA
   ============================ */
    const SITE_INDEX = [
        // Exemplos – você pode ir aumentando essa lista

        // Matérias da revista (revista.html)
        {
            title: "Review – Naked urbana 300cc",
            description: "Avaliação completa da moto urbana 300cc, consumo, conforto e uso diário.",
            type: "materia",
            category: "review",
            url: "revista.html", // se tiver página própria depois, mude o link
        },
        {
            title: "Scooters elétricas na cidade",
            description: "Análise do uso de scooters EV no dia a dia e custo por km.",
            type: "materia",
            category: "eletrico",
            url: "revista.html",
        },

        // Vídeos da TV (tv.html – galeria)
        {
            title: "Cassetadas · Episódio 01",
            description: "Quedas, erros e situações inusitadas em duas rodas.",
            type: "video_tv",
            category: "cassetadas",
            videoId: "dQw4w9WgXcQ", 
            url: "tv.html?v=dQw4w9WgXcQ",
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
            videoId: "dQw4w9WgXcQ",
            url: "tv.html?v=dQw4w9WgXcQ",
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



});
