document.addEventListener("DOMContentLoaded", () => {
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
});
