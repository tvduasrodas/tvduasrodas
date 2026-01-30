// ============================
// CONFIG GITHUB / CMS
// ============================
const REPO_OWNER = "tvduasrodas";
const REPO_NAME = "tvduasrodas";
const NEWS_PATH = "content/news";
const SEARCH_VIDEOS_PATH = "content/videos";

async function fetchJson(url) {
    // Prefixo das chamadas ao GitHub "contents"
    const ghPrefix = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/`;

    // Se a URL for do tipo "contents/..." do GitHub,
    // vamos passar pelo Worker tvduasrodas.com/api/github-list
    if (url.startsWith(ghPrefix)) {
        try {
            // Ex.: url = "https://api.github.com/repos/.../contents/content/news?ref=main"
            const pathWithQuery = url.slice(ghPrefix.length);      // "content/news?ref=main"
            const pathOnly = pathWithQuery.split("?")[0];          // "content/news"

            const workerUrl = `https://tvduasrodas.com/api/github-list?path=${encodeURIComponent(pathOnly)}`;

            const resp = await fetch(workerUrl);
            if (!resp.ok) {
                console.error("Worker retornou erro:", resp.status, workerUrl);
                throw new Error("Worker falhou");
            }

            return resp.json();
        } catch (e) {
            // Se o Worker falhar, faz fallback para o GitHub direto
            console.error("Erro ao usar o Worker, tentando GitHub direto:", e);
        }
    }

    // Comportamento padrão (GitHub direto ou qualquer outra URL JSON)
    const resp = await fetch(url);
    if (!resp.ok) {
        throw new Error("Erro ao buscar: " + url);
    }
    return resp.json();
}

async function fetchText(url) {
    const resp = await fetch(url);
    if (!resp.ok) {
        throw new Error("Erro ao buscar texto: " + url);
    }
    return resp.text();
}

// Parse simples de frontmatter YAML
function parseFrontMatter(markdown) {
    if (!markdown.startsWith("---")) {
        return { data: {}, content: markdown };
    }
    const endIndex = markdown.indexOf("\n---", 3);
    if (endIndex === -1) {
        return { data: {}, content: markdown };
    }

    const fmRaw = markdown.slice(3, endIndex).trim();
    const body = markdown.slice(endIndex + 4).trim();
    const data = {};

    fmRaw.split("\n").forEach((line) => {
        const idx = line.indexOf(":");
        if (idx === -1) return;
        const key = line.slice(0, idx).trim();
        let value = line.slice(idx + 1).trim();
        // tira aspas simples ou duplas
        value = value.replace(/^['"]|['"]$/g, "");
        data[key] = value;
    });

    return { data, content: body };
}

function markdownToExcerpt(markdown, limit = 220) {
    const text = markdown
        .replace(/```[\s\S]*?```/g, "") // blocos de código
        .replace(/`([^`]+)`/g, "$1")
        .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1") // links [texto](url)
        .replace(/[#>*_`-]/g, "")
        .replace(/\r?\n+/g, " ")
        .trim();

    if (text.length <= limit) return text;
    return text.slice(0, limit).replace(/\s+\S*$/, "") + "...";
}

function normalizeCategory(cat) {
    if (!cat) return "outro";
    const c = cat.toLowerCase();

    if (c.includes("moto")) return "motos";
    if (c.includes("lancamentos")) return "lancamentos";
    if (c.includes("bikes")) return "bikes";
    if (c.includes("viagem")) return "viagem";
    if (c.includes("urbano")) return "urbano";
    if (c.includes("test")) return "tests";

    return "outro";
}

// ============================
// ARTIGO – TRANSFORMAR URLs EM LINKS
// ============================
function linkifyArticleBody() {
    const container = document.getElementById("articleBody");
    if (!container) return;

    const urlRegex = /\b((https?:\/\/[^\s<]+)|(www\.[^\s<]+))/gi;

    function walk(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            const text = node.textContent;
            if (!urlRegex.test(text)) return;

            const frag = document.createDocumentFragment();
            let lastIndex = 0;

            text.replace(urlRegex, (match, _full, _httpPart, _wwwPart, offset) => {
                if (offset > lastIndex) {
                    frag.appendChild(
                        document.createTextNode(text.slice(lastIndex, offset))
                    );
                }

                const a = document.createElement("a");
                let href = match;

                if (!/^https?:\/\//i.test(href)) {
                    href = "https://" + href;
                }

                a.href = href;
                a.target = "_blank";
                a.rel = "noopener noreferrer";
                a.textContent = match;

                frag.appendChild(a);
                lastIndex = offset + match.length;
            });

            if (lastIndex < text.length) {
                frag.appendChild(document.createTextNode(text.slice(lastIndex)));
            }

            node.parentNode.replaceChild(frag, node);
        }
        else if (
            node.nodeType === Node.ELEMENT_NODE &&
            node.tagName !== "A" &&
            node.tagName !== "SCRIPT" &&
            node.tagName !== "STYLE"
        ) {
            Array.from(node.childNodes).forEach(walk);
        }
    }

    walk(container);
}


function formatDatePtBr(iso) {
    if (!iso) return "";
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return iso;
    return d.toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "short",
        year: "numeric",
    });
}

function getSlugFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get("slug");
}

// ============================
// REVISTA – PAGINAÇÃO DO GRID
// ============================
let revistaCardsAll = [];
let revistaCurrentPage = 1;
const revistaPerPage = 6;
let revistaCurrentFilter = "all";

function getFilteredRevistaCards() {
    if (!revistaCardsAll.length) return [];
    if (revistaCurrentFilter === "all") return revistaCardsAll;

    return revistaCardsAll.filter(
        (card) => card.getAttribute("data-category") === revistaCurrentFilter
    );
}

function renderRevistaPagination(totalPages) {
    const paginationContainer = document.getElementById("revistaPagination");
    if (!paginationContainer) return;

    paginationContainer.innerHTML = "";

    // Se só tem 1 página, não mostra nada
    if (totalPages <= 1) return;

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "tv-page-btn" + (i === revistaCurrentPage ? " active" : "");
        btn.textContent = i;
        btn.dataset.page = i;

        btn.addEventListener("click", () => {
            revistaCurrentPage = i;
            renderRevistaGrid();
        });

        paginationContainer.appendChild(btn);
    }
}

function renderRevistaGrid() {
    const articleGrid = document.getElementById("articleGrid");
    if (!articleGrid || !revistaCardsAll.length) return;

    const filtered = getFilteredRevistaCards();
    const totalPages = Math.max(1, Math.ceil(filtered.length / revistaPerPage));

    if (revistaCurrentPage > totalPages) {
        revistaCurrentPage = totalPages;
    }

    const start = (revistaCurrentPage - 1) * revistaPerPage;
    const end = start + revistaPerPage;

    // Esconde todos
    revistaCardsAll.forEach((card) => {
        card.style.display = "none";
    });

    // Mostra apenas os da página atual
    filtered.slice(start, end).forEach((card) => {
        card.style.display = "";
    });

    renderRevistaPagination(totalPages);
}


// ============================
// REVISTA – CARREGAR MATÉRIAS DO CMS
// ============================
async function loadMagazineFromCMS() {
    const articleGrid = document.getElementById("articleGrid");
    if (!articleGrid) return; // não está na revista

    const loadingEl = document.getElementById("articleGridLoading");

    try {
        // Lista de arquivos em content/news
        const apiListUrl = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${NEWS_PATH}?ref=main`;
        const files = await fetchJson(apiListUrl);

        // pega só .md
        const mdFiles = files.filter((f) => f.name.endsWith(".md"));

        const artigos = [];

        for (const file of mdFiles) {
            const raw = await fetchText(file.download_url);
            const { data, content } = parseFrontMatter(raw);

            const slug = file.name.replace(/\.md$/, "");
            const title = data.title || slug;

            const categoryRaw = data.category || "";
            const categoryNormalized = normalizeCategory(categoryRaw);

            const date = data.date || "";
            const author = data.author || "TVDUASRODAS";

            const cover = data.cover || "";
            const thumbnail = data.thumbnail || "";
            let videoId = (data.videoId || "").trim();
            videoId = videoId.replace(/^['"]+|['"]+$/g, "");
            if (videoId === "''") videoId = "";

            const featured =
                String(data.featured || "").toLowerCase() === "true";

            const excerpt = markdownToExcerpt(content, 220);

            // decide qual imagem usar (para cards e, se quiser, para hero também)
            let imgSrc = "";
            if (thumbnail) {
                imgSrc = thumbnail;
            } else if (cover) {
                imgSrc = cover;
            } else if (videoId) {
                imgSrc = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
            }

            artigos.push({
                slug,
                title,
                categoryRaw,
                categoryNormalized,
                date,
                author,
                imgSrc,
                excerpt,
                videoId,
                featured,
            });
        }

        // ordena por data desc (mais recente primeiro)
        artigos.sort((a, b) => (a.date < b.date ? 1 : -1));

        // define qual artigo vai para a HERO:
        let heroArticle = artigos.find((a) => a.featured);
        if (!heroArticle && artigos.length) {
            heroArticle = artigos[0]; // fallback: mais recente
        }

        // Renderiza a HERO
        if (heroArticle) {
            renderMagazineHero(heroArticle);
        }

        // Monta o GRID, pulando o hero (para não duplicar)
        articleGrid.innerHTML = "";

        artigos.forEach((artigo) => {
            if (heroArticle && artigo.slug === heroArticle.slug) return;

            const card = document.createElement("article");
            card.className = "card article-card";
            card.dataset.category = artigo.categoryNormalized;

            const linkHref = `materia.html?slug=${encodeURIComponent(artigo.slug)}`;
            const categoriaLabel = artigo.categoryRaw || "Matéria";

            let coverHtml = "";
            if (artigo.imgSrc) {
                coverHtml = `
                    <div class="article-card-cover">
                        <img src="${artigo.imgSrc}" alt="${artigo.title}">
                    </div>
                `;
            }

            card.innerHTML = `
                ${coverHtml}
                <span class="category-tag">${categoriaLabel}</span>
                <h3>
                    <a href="${linkHref}">
                        ${artigo.title}
                    </a>
                </h3>
                ${artigo.excerpt ? `<p>${artigo.excerpt}</p>` : ""}
                <a href="${linkHref}" class="article-link">
                    Ler matéria &rarr;
                </a>
            `;

            articleGrid.appendChild(card);
        });

        // Atualiza array global de cards e reseta paginação
        revistaCardsAll = Array.from(articleGrid.querySelectorAll(".article-card"));
        revistaCurrentPage = 1;
        revistaCurrentFilter = "all";

        // Renderiza o grid paginado (máx. 6 por página)
        renderRevistaGrid();

        if (!artigos.length && loadingEl) {
            loadingEl.textContent = "Nenhuma matéria cadastrada ainda.";
        }
    } catch (err) {
        console.error(err);
        if (loadingEl) {
            loadingEl.textContent = "Não foi possível carregar as matérias agora.";
        }
    }
}

async function loadMoreArticlesSidebar() {
    const sidebarRev = document.getElementById("moreArticlesSidebarRevista");
    const sidebarMat = document.getElementById("moreArticlesSidebarMateria");

    // Se nenhuma das duas páginas tiver o bloco, não faz nada
    if (!sidebarRev && !sidebarMat) return;

    try {
        // Lista de arquivos em content/news
        const apiListUrl = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${NEWS_PATH}?ref=main`;
        const files = await fetchJson(apiListUrl);

        // pega só .md
        const mdFiles = files.filter((f) => f.name.endsWith(".md"));

        const artigos = [];

        for (const file of mdFiles) {
            const slug = file.name.replace(/\.md$/, "");
            const localUrl = `${NEWS_PATH}/${slug}.md`; // ex: content/news/minha-materia.md

            try {
                const raw = await fetchText(localUrl);
                const { data, content } = parseFrontMatter(raw);

                const title = data.title || slug;
                const categoryRaw = data.category || "";
                const date = data.date || "";

                artigos.push({
                    slug,
                    title,
                    categoryRaw,
                    date,
                    excerpt: markdownToExcerpt(content, 160),
                });
            } catch (err) {
                console.warn("Falha ao carregar matéria da sidebar:", localUrl, err);
                // se um arquivo der erro, segue pros próximos sem quebrar tudo
                continue;
            }
        }


        if (!artigos.length) {
            if (sidebarRev) sidebarRev.innerHTML = "<li>Nenhuma matéria encontrada.</li>";
            if (sidebarMat) sidebarMat.innerHTML = "<li>Nenhuma matéria encontrada.</li>";
            return;
        }

        // se estiver na página de matéria, evita repetir a matéria atual
        const currentSlug = getSlugFromUrl(); // já existe no main.js
        let candidatos = artigos;
        if (currentSlug) {
            candidatos = artigos.filter((a) => a.slug !== currentSlug);
            if (!candidatos.length) {
                candidatos = artigos; // fallback: se só tiver 1 matéria
            }
        }

        // embaralha (aleatório)
        candidatos.sort(() => Math.random() - 0.5);

        // pega 4
        const selecionados = candidatos.slice(0, 4);

        const html = selecionados
            .map((artigo) => {
                const href = `materia.html?slug=${encodeURIComponent(artigo.slug)}`;
                return `<li><a href="${href}">${artigo.title}</a></li>`;
            })
            .join("");

        if (sidebarRev) {
            sidebarRev.innerHTML = html;
        }
        if (sidebarMat) {
            sidebarMat.innerHTML = html;
        }
    } catch (err) {
        console.error("Erro ao carregar Mais matérias:", err);
        if (sidebarRev) {
            sidebarRev.innerHTML = "<li>Não foi possível carregar as matérias agora.</li>";
        }
        if (sidebarMat) {
            sidebarMat.innerHTML = "<li>Não foi possível carregar as matérias agora.</li>";
        }
    }
}



function renderMagazineHero(article) {
    const hero = document.getElementById("revistaHero");
    if (!hero || !article) return;

    const linkEl = document.getElementById("revistaHeroLink");
    const imgEl = document.getElementById("revistaHeroImage");
    const catEl = document.getElementById("revistaHeroCategory");
    const titleEl = document.getElementById("revistaHeroTitle");
    const excerptEl = document.getElementById("revistaHeroExcerpt");
    const authorEl = document.getElementById("revistaHeroAuthor");
    const dateEl = document.getElementById("revistaHeroDate");
    const readMoreEl = document.getElementById("revistaHeroReadMore");

    const url = `materia.html?slug=${encodeURIComponent(article.slug)}`;

    if (linkEl) linkEl.href = url;
    if (readMoreEl) readMoreEl.href = url;

    if (titleEl) {
        titleEl.href = url;
        titleEl.textContent = article.title || "Matéria em destaque";
    }

    if (catEl) {
        catEl.textContent = article.categoryRaw || "Matéria";
    }

    if (excerptEl) {
        excerptEl.textContent = article.excerpt || "";
    }

    if (authorEl) {
        authorEl.textContent = article.author
            ? "Por " + article.author
            : "";
    }

    if (dateEl) {
        dateEl.textContent = article.date
            ? "Publicado em " + formatDatePtBr(article.date)
            : "";
    }

    // Escolhe imagem da hero:
    // 1) thumbnailHero (se você quiser diferenciar)
    // 2) thumbnail / cover
    // 3) thumb do YouTube
    let heroImgSrc = article.heroImgSrc || article.imgSrc || "";

    if (!heroImgSrc && article.videoId) {
        heroImgSrc = `https://img.youtube.com/vi/${article.videoId}/hqdefault.jpg`;
    }

    if (imgEl && heroImgSrc) {
        imgEl.src = heroImgSrc;
        imgEl.alt = article.title || "";
    }
}

// ============================
// HOME – ÚLTIMAS MATÉRIAS DA REVISTA (index.html)
// ============================
async function loadHomeLatestArticles() {
    const grid = document.getElementById("latest-articles-grid");
    if (!grid) return; // não está na home

    try {
        const apiListUrl = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${NEWS_PATH}?ref=main`;
        const files = await fetchJson(apiListUrl);

        const mdFiles = Array.isArray(files)
            ? files.filter((f) => f.type === "file" && f.name.endsWith(".md"))
            : [];

        const artigos = [];

        for (const file of mdFiles) {
            const raw = await fetchText(file.download_url);
            const { data, content } = parseFrontMatter(raw);

            const slug = file.name.replace(/\.md$/, "");
            const title = data.title || slug;

            const categoryRaw = data.category || "";
            const date = data.date || "";

            const cover = data.cover || "";
            const thumbnail = data.thumbnail || "";
            let videoId = (data.videoId || "").trim();
            videoId = videoId.replace(/^['"]+|['"]+$/g, "");
            if (videoId === "''") videoId = "";

            const excerpt = markdownToExcerpt(content, 200);

            // Mesma lógica da revista: thumb > cover > thumb do YouTube
            let imgSrc = "";
            if (thumbnail) {
                imgSrc = thumbnail;
            } else if (cover) {
                imgSrc = cover;
            } else if (videoId) {
                imgSrc = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
            }

            artigos.push({
                slug,
                title,
                categoryRaw,
                date,
                excerpt,
                imgSrc,
            });
        }

        if (!artigos.length) {
            grid.innerHTML = "<p>Nenhuma matéria cadastrada ainda.</p>";
            return;
        }

        // Mais recentes primeiro
        artigos.sort(
            (a, b) => new Date(b.date || 0) - new Date(a.date || 0)
        );

        const top = artigos.slice(0, 4); // mostra 4 cards na home
        grid.innerHTML = "";

        top.forEach((artigo) => {
            const card = document.createElement("article");
            card.className = "card article-card";

            const linkHref = `materia.html?slug=${encodeURIComponent(
                artigo.slug
            )}`;
            const categoriaLabel = artigo.categoryRaw || "Matéria";

            let coverHtml = "";
            if (artigo.imgSrc) {
                coverHtml = `
                    <div class="article-card-cover">
                        <img src="${artigo.imgSrc}" alt="${artigo.title}">
                    </div>
                `;
            }

            card.innerHTML = `
                ${coverHtml}
                <span class="category-tag">${categoriaLabel}</span>
                <h3>
                    <a href="${linkHref}">
                        ${artigo.title}
                    </a>
                </h3>
                ${artigo.excerpt
                    ? `<p>${artigo.excerpt}</p>`
                    : ""
                }
                <a href="${linkHref}" class="article-link">
                    Ler matéria &rarr;
                </a>
            `;

            grid.appendChild(card);
        });
    } catch (e) {
        console.error("Erro ao carregar últimas matérias da home", e);
        grid.innerHTML =
            "<p>Não foi possível carregar as matérias agora.</p>";
    }
}


// ============================
// HOME – ÚLTIMOS VÍDEOS + VÍDEOS EM DESTAQUE (index.html)
// ============================

// Helper só para esta função: extrai ID de URL do YouTube
function extractYouTubeId(url) {
    if (!url) return "";
    try {
        const u = new URL(url);

        // youtu.be/ID
        if (u.hostname.includes("youtu.be")) {
            return u.pathname.replace("/", "").trim();
        }

        // youtube.com/watch?v=ID
        const v = u.searchParams.get("v");
        if (v) return v.trim();
    } catch (e) {
        // Se não for uma URL válida, tenta um fallback simples
    }

    // Fallback: pega o último "pedaço" depois de / ou =
    const parts = url.split(/\/|=|\?/).filter(Boolean);
    return parts.length ? parts[parts.length - 1].trim() : "";
}

async function loadHomeVideos() {
    const latestGrid = document.getElementById("latest-videos-grid");
    const featuredGrid = document.getElementById("featured-videos-grid");

    // Se não estiver na home, não faz nada
    if (!latestGrid && !featuredGrid) return;

    try {
        const apiListUrl = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${SEARCH_VIDEOS_PATH}?ref=main`;
        const files = await fetchJson(apiListUrl);

        const mdFiles = Array.isArray(files)
            ? files.filter((f) => f.type === "file" && f.name.endsWith(".md"))
            : [];

        const videos = [];

        for (const file of mdFiles) {
            const raw = await fetchText(file.download_url);
            const { data, content } = parseFrontMatter(raw);

            const slug = file.name.replace(/\.md$/, "");
            const title = data.title || slug;
            const category = data.category || "";
            const date = data.date || "";

            const cover = data.cover || "";
            const thumbnail = data.thumbnail || "";

            // Lê youtube/youtube_url
            const youtube = data.youtube_url || data.youtube || "";

            // 1) tenta pegar do campo videoId
            let videoId = (data.videoId || "").trim();
            videoId = videoId.replace(/^['"]+|['"]+$/g, "");
            if (videoId === "''") videoId = "";

            // 2) se não tiver videoId, extrai do youtube
            if (!videoId && youtube) {
                videoId = extractYouTubeId(youtube);
            }

            const excerpt = markdownToExcerpt(content, 160);
            const featuredFlag =
                String(data.featured || "").toLowerCase() === "true";

            // Thumb para o vídeo:
            // 1) YouTube (se tiver videoId) → 2) thumbnail → 3) cover
            let thumbUrl = "";
            if (videoId) {
                thumbUrl = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
            } else if (thumbnail) {
                thumbUrl = thumbnail;
            } else if (cover) {
                thumbUrl = cover;
            }

            const url = videoId
                ? `tv.html?v=${encodeURIComponent(videoId)}`
                : youtube || "tv.html";

            videos.push({
                slug,
                title,
                category,
                date,
                videoId,
                youtube,
                excerpt,
                featured: featuredFlag,
                thumbUrl,
                url,
            });
        }

        if (!videos.length) {
            if (latestGrid) {
                latestGrid.innerHTML =
                    "<p>Nenhum vídeo cadastrado ainda.</p>";
            }
            if (featuredGrid) {
                featuredGrid.innerHTML =
                    "<p>Nenhum vídeo em destaque ainda.</p>";
            }
            return;
        }

        // Mais recentes primeiro
        videos.sort(
            (a, b) => new Date(b.date || 0) - new Date(a.date || 0)
        );

        // ---------- "Últimos vídeos" – SOMENTE 3 ----------
        if (latestGrid) {
            latestGrid.innerHTML = "";
            const latest = videos.slice(0, 3); // 3 vídeos

            latest.forEach((video) => {
                const card = document.createElement("article");
                card.className = "card video-card tv-video-card";

                // Usa .video-thumb.real-thumb + <img> para usar seu CSS de PLAY
                const thumbHtml = video.thumbUrl
                    ? `
                    <a href="${video.url}" class="video-thumb real-thumb">
                        <img src="${video.thumbUrl}" alt="${video.title}">
                    </a>
                `
                    : `
                    <a href="${video.url}" class="video-thumb placeholder small">
                        <span>Ver vídeo</span>
                    </a>
                `;

                card.innerHTML = `
                    ${thumbHtml}
                    <div class="video-info">
                        <span class="category-tag">${video.category || "Vídeo"}</span>
                        <h3><a href="${video.url}">${video.title}</a></h3>
                        ${video.excerpt ? `<p>${video.excerpt}</p>` : ""}
                    </div>
                `;

                latestGrid.appendChild(card);
            });
        }

        // ---------- "Vídeos em destaque" ----------
        if (featuredGrid) {
            featuredGrid.innerHTML = "";

            const featuredVideos = videos.filter((v) => v.featured);
            const list =
                featuredVideos.length > 0
                    ? featuredVideos
                    : videos.slice(0, 3); // também 3 por padrão

            list.forEach((video) => {
                const card = document.createElement("article");
                card.className = "card video-card tv-video-card";

                const thumbHtml = video.thumbUrl
                    ? `
                    <a href="${video.url}" class="video-thumb real-thumb">
                        <img src="${video.thumbUrl}" alt="${video.title}">
                    </a>
                `
                    : `
                    <a href="${video.url}" class="video-thumb placeholder small">
                        <span>Ver vídeo</span>
                    </a>
                `;

                card.innerHTML = `
                    ${thumbHtml}
                    <div class="video-info">
                        <span class="category-tag">${video.category || "Vídeo"}</span>
                        <h3><a href="${video.url}">${video.title}</a></h3>
                        ${video.excerpt ? `<p>${video.excerpt}</p>` : ""}
                    </div>
                `;

                featuredGrid.appendChild(card);
            });
        }
    } catch (e) {
        console.error("Erro ao carregar vídeos da home", e);
        if (latestGrid) {
            latestGrid.innerHTML =
                "<p>Não foi possível carregar os vídeos agora.</p>";
        }
        if (featuredGrid) {
            featuredGrid.innerHTML =
                "<p>Não foi possível carregar os vídeos em destaque agora.</p>";
        }
    }
}




document.addEventListener("DOMContentLoaded", () => {

    // HOME – carrega últimas matérias e vídeos (se os grids existirem na página)
    loadHomeLatestArticles();

    /* ============================
       FILTRO DE MATÉRIAS (REVISTA)
       ============================ */
    const filterButtons = document.querySelectorAll(".filter-btn");
    const articleGrid = document.getElementById("articleGrid");

    if (filterButtons.length && articleGrid) {
        filterButtons.forEach((btn) => {
            btn.addEventListener("click", () => {
                const filter = btn.getAttribute("data-filter") || "all";

                // Atualiza estado visual do botão
                filterButtons.forEach((b) => b.classList.remove("active"));
                btn.classList.add("active");

                // Atualiza filtro global e reseta para a página 1
                revistaCurrentFilter = filter;
                revistaCurrentPage = 1;

                // Re-renderiza o grid com base no filtro + paginação
                renderRevistaGrid();
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
        /* ============================
       PÁGINA DE RESULTADOS DE BUSCA (busca.html)
       ============================ */
    const searchResultsContainer = document.getElementById("searchResults");
    const searchSummary = document.getElementById("searchSummary");
    const headerSearchInput = document.getElementById("siteSearchInput");
    const headerSearchClear = document.getElementById("siteSearchClear");

    // --- Helpers da busca no CMS (matérias + vídeos) ---

    async function loadSearchEntriesFromPath(path, type) {
        const apiListUrl = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${path}?ref=main`;

        let files = [];
        try {
            files = await fetchJson(apiListUrl);
        } catch (e) {
            console.error("Erro ao listar arquivos para busca em", path, e);
            return [];
        }

        if (!Array.isArray(files)) return [];

        const mdFiles = files.filter((f) => f.type === "file" && f.name.endsWith(".md"));
        const entries = [];

        for (const file of mdFiles) {
            try {
                const raw = await fetchText(file.download_url);
                const { data, content } = parseFrontMatter(raw);

                const slug = file.name.replace(/\.md$/, "");
                const title = data.title || slug;
                const category = data.category || "";
                const date = data.date || "";

                const thumbnail = data.thumbnail || data.cover || "";

                let videoId = (data.videoId || "").trim();
                videoId = videoId.replace(/^['"]+|['"]+$/g, "");
                if (videoId === "''") videoId = "";

                const youtube = data.youtube_url || data.youtube || "";

                // Agora: se NÃO tiver videoId, sempre tenta extrair do YouTube,
                // tanto para vídeos quanto para matérias
                if (!videoId && youtube) {
                    videoId = extractYouTubeId(youtube);
                }


                const excerpt = markdownToExcerpt(content, 180);

                let url = "#";
                if (type === "materia") {
                    url = `materia.html?slug=${encodeURIComponent(slug)}`;
                } else if (type === "video") {
                    if (videoId) {
                        url = `tv.html?v=${encodeURIComponent(videoId)}`;
                    } else if (youtube) {
                        url = youtube;
                    } else {
                        url = "tv.html";
                    }
                }

                entries.push({
                    type,
                    slug,
                    title,
                    category,
                    date,
                    thumbnail,
                    videoId,
                    youtube,
                    excerpt,
                    content,
                    url,
                });
            } catch (e) {
                console.error("Erro ao carregar arquivo de busca", file.name, e);
            }
        }

        return entries;
    }

    async function buildCmsSearchIndex() {
        // sempre inclui matérias
        const promises = [loadSearchEntriesFromPath(NEWS_PATH, "materia")];

        // também inclui vídeos do CMS (content/videos) para a busca
        if (typeof SEARCH_VIDEOS_PATH !== "undefined") {
            promises.push(loadSearchEntriesFromPath(SEARCH_VIDEOS_PATH, "video"));
        }

        const resultsByType = await Promise.all(promises);
        const all = resultsByType.flat();

        // ordena por data (mais recente primeiro)
        all.sort((a, b) => {
            const da = new Date(a.date || 0);
            const db = new Date(b.date || 0);
            return db - da;
        });

        return all;
    }


    function renderSearchResultCard(item) {
        const isVideo = item.type === "video";
        const typeLabel = isVideo ? "Vídeo" : "Matéria";
        const categoryText = item.category ? " · " + item.category : "";

        let thumbUrl = "";

        if (isVideo) {
            // Vídeos: 1) thumb YouTube (videoId) 2) thumbnail/cover
            if (item.videoId) {
                thumbUrl = `https://img.youtube.com/vi/${item.videoId}/hqdefault.jpg`;
            } else if (item.thumbnail) {
                thumbUrl = item.thumbnail;
            }
        } else {
            // Matérias: 1) thumbnail/cover 2) se não tiver, usa thumb automático do YouTube se tiver vídeo
            if (item.thumbnail) {
                thumbUrl = item.thumbnail;
            } else if (item.videoId) {
                thumbUrl = `https://img.youtube.com/vi/${item.videoId}/hqdefault.jpg`;
            }
        }

        let thumbHtml = "";

        if (thumbUrl) {
            if (isVideo) {
                // Vídeo: com ícone de play
                thumbHtml = `
                <div class="search-video-thumb"
                     style="background-image:url('${thumbUrl}');background-size:cover;background-position:center;">
                    <span class="search-play-icon"></span>
                </div>
            `;
            } else {
                // Matéria: sem ícone de play
                thumbHtml = `
                <div class="search-video-thumb"
                     style="background-image:url('${thumbUrl}');background-size:cover;background-position:center;">
                </div>
            `;
            }
        }

        const text = item.excerpt || "Clique para ver mais.";

        return `
      <article class="card article-card ${isVideo ? "search-video-card" : ""}">
        <span class="category-tag">
          ${typeLabel}${categoryText}
        </span>
        ${thumbHtml}
        <h3>${item.title}</h3>
        <p>${text}</p>
        <a href="${item.url}" class="article-link">
          ${isVideo ? "Assistir vídeo" : "Ler matéria"} &rarr;
        </a>
      </article>
    `;
    }


    // --- Controle do botão "x" em QUALQUER página ---
    if (headerSearchInput && headerSearchClear) {
        const updateClearVisibility = () => {
            headerSearchClear.style.display = headerSearchInput.value ? "block" : "none";
        };
        updateClearVisibility();

        headerSearchInput.addEventListener("input", updateClearVisibility);
    }

    // --- Lógica específica da página busca.html ---
    if (searchResultsContainer && searchSummary) {
        const params = new URLSearchParams(window.location.search);
        const termRaw = params.get("q") || "";
        const term = termRaw.trim().toLowerCase();

        // Preenche o campo de busca no header com o termo atual
        if (headerSearchInput) {
            headerSearchInput.value = termRaw;
        }

        // Na página busca.html, o "x" limpa e volta para busca vazia
        if (headerSearchClear && headerSearchInput) {
            headerSearchClear.style.display = termRaw ? "block" : "none";
            headerSearchClear.addEventListener("click", () => {
                headerSearchInput.value = "";
                window.location.href = "busca.html";
            });
        }

        if (!term) {
            searchSummary.textContent =
                "Digite um termo na barra de busca acima para encontrar matérias e vídeos da TV Duas Rodas.";
            searchResultsContainer.innerHTML = "";
        } else {
            searchSummary.textContent = `Buscando por “${termRaw}” em matérias e vídeos...`;
            searchResultsContainer.innerHTML = "";

            (async () => {
                try {
                    const all = await buildCmsSearchIndex();

                    const results = all.filter((item) => {
                        const haystack = (
                            (item.title || "") +
                            " " +
                            (item.category || "") +
                            " " +
                            (item.excerpt || "") +
                            " " +
                            (item.content || "")
                        ).toLowerCase();

                        return haystack.includes(term);
                    });

                    if (!results.length) {
                        searchSummary.textContent = `Nenhum resultado encontrado para “${termRaw}”.`;
                        searchResultsContainer.innerHTML = "";
                    } else {
                        searchSummary.textContent = `Encontrados ${results.length} resultado(s) para “${termRaw}”.`;
                        searchResultsContainer.innerHTML = results
                            .map((item) => renderSearchResultCard(item))
                            .join("");
                    }
                } catch (e) {
                    console.error("Erro na busca CMS:", e);
                    searchSummary.textContent =
                        `Não foi possível buscar por “${termRaw}” agora. Tente novamente mais tarde.`;
                    searchResultsContainer.innerHTML = "";
                }
            })();
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


    // ============================
    // HELPERS PARA MATÉRIA (MD + FRONTMATTER)
    // ============================

    function parseFrontmatterArticle(text) {
        const result = {
            title: "",
            date: "",
            category: "",
            author: "",
            summary: "",
            kicker: "",
            tagline: "",
            readingTime: "",
            sponsor: "",
            thumbnail: "",
            videoId: "",
            body: "",
        };

        if (!text.startsWith("---")) {
            result.body = text.trim();
            return result;
        }

        const second = text.indexOf("---", 3);
        if (second === -1) {
            result.body = text.trim();
            return result;
        }

        const fmRaw = text.slice(3, second).trim();
        const body = text.slice(second + 3).trim();
        result.body = body;

        fmRaw.split("\n").forEach((line) => {
            const [key, ...rest] = line.split(":");
            if (!key || !rest.length) return;
            const k = key.trim();
            let v = rest.join(":").trim();
            // remove aspas simples ou duplas no começo/fim: "valor", 'valor', '' etc.
            v = v.replace(/^['"]|['"]$/g, "");

            if (k === "title") result.title = v;
            else if (k === "date") result.date = v;
            else if (k === "category") result.category = v;
            else if (k === "author") result.author = v;
            else if (k === "summary") result.summary = v;
            else if (k === "kicker") result.kicker = v;
            else if (k === "tagline") result.tagline = v;
            else if (k === "readingTime") result.readingTime = v;
            else if (k === "sponsor") result.sponsor = v;
            else if (k === "thumbnail") result.thumbnail = v;
            else if (k === "videoId") result.videoId = v;
            else if (k === "cover") result.cover = v;
            else {
                // guarda qualquer outro campo extra, se existir
                result[k] = v;
            }
        });

        return result;
    }

    function markdownToHtml(md) {
        const lines = md.split(/\r?\n/);
        const html = [];
        let inList = false;

        for (let rawLine of lines) {
            let line = rawLine.trim();

            // Linha em branco → fecha lista se estiver aberta
            if (!line) {
                if (inList) {
                    html.push("</ul>");
                    inList = false;
                }
                continue;
            }

            // IMAGEM sozinha na linha: ![alt](url)
            const imgMatch = line.match(/^!\[([^\]]*)\]\(([^)]+)\)/);
            if (imgMatch) {
                if (inList) {
                    html.push("</ul>");
                    inList = false;
                }

                const alt = imgMatch[1] || "";
                const src = imgMatch[2];

                html.push(`
                <figure class="article-inline-media">
                    <img src="${src}" alt="${alt}">
                </figure>
            `);
                continue;
            }

            // LISTA com - ou *
            if (/^[-*]\s+/.test(line)) {
                if (!inList) {
                    html.push("<ul>");
                    inList = true;
                }
                const item = line.replace(/^[-*]\s+/, "");
                html.push(`<li>${item}</li>`);
                continue;
            } else if (inList) {
                html.push("</ul>");
                inList = false;
            }

            // TÍTULOS
            if (/^###\s+/.test(line)) {
                html.push(`<h3>${line.replace(/^###\s+/, "")}</h3>`);
            } else if (/^##\s+/.test(line)) {
                html.push(`<h2>${line.replace(/^##\s+/, "")}</h2>`);
            } else if (/^#\s+/.test(line)) {
                html.push(`<h1>${line.replace(/^#\s+/, "")}</h1>`);
            } else {
                // PARÁGRAFO normal
                html.push(`<p>${line}</p>`);
            }
        }

        if (inList) {
            html.push("</ul>");
        }

        return html.join("\n");
    }


    function formatArticleDate(str) {
        if (!str) return "";
        const d = new Date(str);
        if (isNaN(d.getTime())) {
            // Se não for uma data válida, devolve como veio
            return str;
        }
        const meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
        const dia = String(d.getDate()).padStart(2, "0");
        const mes = meses[d.getMonth()];
        const ano = d.getFullYear();
        return `${dia} ${mes} ${ano}`;
    }


    /* ============================
    CARREGAMENTO DE MATÉRIA DINÂMICA (materia?slug=...)
    AGORA LENDO /content/news/<slug>.md
    ============================ */

    const articleMain = document.getElementById("articleMain");

    if (articleMain) {
        const params = new URLSearchParams(window.location.search);
        const slug = params.get("slug");

        if (!slug) {
            const titleEl = document.getElementById("articleTitle");
            const bodyEl = document.getElementById("articleBody");
            if (titleEl) titleEl.textContent = "Matéria não encontrada";
            if (bodyEl) {
                bodyEl.innerHTML =
                    "<p>Slug não informado na URL. Use <code>?slug=...</code>.</p>";
            }
        } else {
            // Agora buscamos o .md em content/news
            fetch(`content/news/${slug}.md`)
                .then((res) => {
                    if (!res.ok) {
                        throw new Error("Não encontrado");
                    }
                    return res.text();
                })
                .then((rawText) => {
                    const data = parseFrontmatterArticle(rawText);
                    const bodyHtml = markdownToHtml(data.body || "");

                    // ============================
                    // SEO DINÂMICO DA MATÉRIA
                    // ============================

                    // Título da aba (usa o título da matéria)
                    const articleTitle = data.title || "Matéria";
                    document.title = `${articleTitle} | TVDUASRODAS`;

                    // Meta description (usa summary, se tiver, ou gera um resumo do corpo)
                    const articleExcerpt =
                        data.summary && data.summary.trim()
                            ? data.summary.trim()
                            : markdownToExcerpt(data.body || "", 200);

                    let metaDesc = document.querySelector('meta[name="description"]');
                    if (!metaDesc) {
                        metaDesc = document.createElement("meta");
                        metaDesc.setAttribute("name", "description");
                        document.head.appendChild(metaDesc);
                    }
                    metaDesc.setAttribute("content", articleExcerpt);

                    // === CANONICAL SEO (URL oficial da matéria) ===
                    const canonicalUrl = `${window.location.origin}${window.location.pathname}?slug=${encodeURIComponent(
                        data.slug || slug
                    )}`;

                    let canonicalLink = document.querySelector("link[rel='canonical']");
                    if (!canonicalLink) {
                        canonicalLink = document.createElement("link");
                        canonicalLink.setAttribute("rel", "canonical");
                        document.head.appendChild(canonicalLink);
                    }
                    canonicalLink.setAttribute("href", canonicalUrl);



                    // Título da aba
                    document.title = `${data.title || "Matéria"} | TV Duas Rodas`;

                    // Cabeçalho
                    const tag = document.getElementById("articleTag");
                    const titleEl = document.getElementById("articleTitle");
                    const bcTag = document.getElementById("articleBreadcrumbTag");
                    const authorEl = document.getElementById("articleAuthor");
                    const dateEl = document.getElementById("articleDate");
                    const readEl = document.getElementById("articleReadingTime");

                    if (tag) {
                        const baseCat = data.category || "Matéria";
                        const kicker = data.kicker || data.tagline || "";
                        tag.textContent = kicker ? `${baseCat} · ${kicker}` : baseCat;
                    }
                    if (bcTag) bcTag.textContent = data.category || "Matéria";
                    if (titleEl) titleEl.textContent = data.title || "";
                    if (authorEl)
                        authorEl.textContent = data.author
                            ? `Por ${data.author}`
                            : "Por Redação TV Duas Rodas";
                    if (dateEl) dateEl.textContent = formatArticleDate(data.date);
                    if (readEl)
                        readEl.textContent = data.readingTime
                            ? `Leitura: ${data.readingTime}`
                            : "";

                    // Patrocínio (se algum dia você adicionar no frontmatter)
                    const sponsorWrapper = document.getElementById("articleSponsorWrapper");
                    const sponsorEl = document.getElementById("articleSponsor");
                    if (data.sponsor && sponsorWrapper && sponsorEl) {
                        sponsorWrapper.hidden = false;
                        sponsorEl.textContent = data.sponsor;
                    } else if (sponsorWrapper) {
                        sponsorWrapper.hidden = true;
                    }

                    // HERO: vídeo ou imagem
                    const hero = data.hero || {};
                    const heroVideoWrapper = document.getElementById("articleHeroVideo");
                    const heroIframe = document.getElementById("articleHeroIframe");
                    const heroImageWrapper = document.getElementById("articleHeroImage");
                    const heroImageTag = document.getElementById("articleHeroImageTag");
                    const heroCaption = document.getElementById("articleHeroCaption");
                    const ctaContainer = document.getElementById("articleVideoCtaContainer");

                    // 👉 Reset: esconde tudo antes de decidir o que mostrar
                    if (heroVideoWrapper) heroVideoWrapper.hidden = true;
                    if (heroImageWrapper) heroImageWrapper.hidden = true;
                    if (ctaContainer) ctaContainer.innerHTML = "";

                    // 👉 Usa um videoId sanitizado (sem aspas e sem vazio)
                    let videoIdClean = (data.videoId || "").trim();
                    videoIdClean = videoIdClean.replace(/^['"]+|['"]+$/g, "");
                    if (videoIdClean === "''") videoIdClean = "";

                    // 👉 Descobrir qual campo tem a imagem
                    // - JSON antigo: hero.image
                    // - CMS Notícias: cover (campo que existe no seu .md), ou thumbnail, ou image
                    let heroImage = "";
                    if (hero.image) {
                        heroImage = hero.image;
                    } else if (data.cover) {
                        heroImage = data.cover;
                    } else if (data.thumbnail) {
                        heroImage = data.thumbnail;
                    } else if (data.image) {
                        heroImage = data.image;
                    }

                    // 👉 Se tiver videoId válido, hero é VÍDEO
                    if (videoIdClean && heroVideoWrapper && heroIframe) {
                        heroVideoWrapper.hidden = false;
                        heroIframe.src = `https://www.youtube.com/embed/${videoIdClean}`;
                        heroIframe.title = data.title || "Vídeo da matéria";

                        if (ctaContainer) {
                            ctaContainer.innerHTML = `
      <div class="article-video-cta">
        <a href="tv.html?v=${videoIdClean}" class="btn btn-outline btn-small">
          Assistir na TV &amp; Vídeos &rarr;
        </a>
      </div>
    `;
                        }
                    }
                    // 👉 Se NÃO tiver videoId, mas tiver imagem, hero é IMAGEM
                    else if (heroImage && heroImageWrapper && heroImageTag) {
                        heroImageWrapper.hidden = false;
                        heroImageTag.src = heroImage;
                        heroImageTag.alt = (hero.alt || data.title || "").trim();
                        if (heroCaption) {
                            heroCaption.textContent = hero.caption || "";
                        }
                    }                    

                    // Corpo da matéria
                    const bodyEl = document.getElementById("articleBody");
                    if (bodyEl) {
                        bodyEl.innerHTML = bodyHtml || "<p>Sem conteúdo.</p>";
                        linkifyArticleBody();
                    }

                    // Links de compartilhamento
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
                            "<p>Não encontramos a matéria para este link. Verifique o endereço ou volte para a <a href='revista.html'>Revista</a>.</p>";
                    }
                });
        }
    }

    // Dispara carregamento da Revista (lista de matérias)
    loadMagazineFromCMS();
    loadMoreArticlesSidebar();



});
