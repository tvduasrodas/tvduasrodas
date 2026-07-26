(function () {
    "use strict";

    const GOOGLE_ANALYTICS_ID = "G-N47HBZWC5X";
    const CONFIG_URL = "/content/ads/config.json";
    let configPromise;
    let currentContext = {};

    function loadGoogleAnalytics() {
        if (window.__tvduasrodasAnalyticsLoaded) return;
        window.__tvduasrodasAnalyticsLoaded = true;

        window.dataLayer = window.dataLayer || [];
        window.gtag = window.gtag || function () {
            window.dataLayer.push(arguments);
        };
        window.gtag("js", new Date());
        window.gtag("config", GOOGLE_ANALYTICS_ID);

        const script = document.createElement("script");
        script.async = true;
        script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(GOOGLE_ANALYTICS_ID)}`;
        document.head.appendChild(script);
    }

    const normalize = (value) => String(value || "")
        .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        .toLowerCase();

    const esc = (value) => String(value ?? "")
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;").replace(/'/g, "&#39;");

    function pageContext() {
        const path = window.location.pathname.toLowerCase();
        const description = document.querySelector('meta[name="description"]')?.content || "";
        const heading = document.querySelector("main h1")?.textContent || "";
        const mainText = document.querySelector("main")?.innerText?.slice(0, 5000) || "";
        let type = "page";
        let adCategory = "";
        const institutional = [
            "/sobre", "/contato", "/imprensa", "/politica-de-privacidade",
            "/termos", "/busca", "/arquivo", "/revista"
        ].some((segment) => path.includes(segment));
        if (institutional) {
            type = "institutional";
            adCategory = "geral";
        } else if (path.includes("/competicoes/") || /competição|campeonato/i.test(heading)) {
            type = "competition";
            adCategory = "competicoes";
        } else if (path.includes("/eventos/")) {
            type = "event";
            adCategory = "eventos";
        } else if (path.includes("/videos/") || /tv\s*&\s*vídeos/i.test(heading)) {
            type = "video";
        } else if (path.includes("/materias/") || path.includes("/guias/")) {
            type = "article";
        }
        return {
            type,
            ad_category: adCategory,
            title: [document.title, heading].filter(Boolean).join(" "),
            body: [description, mainText].filter(Boolean).join(" ")
        };
    }

    function ensureDefaultSlot(root = document) {
        if (root !== document || document.querySelector("[data-ad-slot]")) return;
        const main = document.querySelector("main");
        if (!main) return;
        const container = main.querySelector(".container") || main;
        const hasSidebarLayout = container.classList.contains("layout-with-sidebar");
        const target = hasSidebarLayout
            ? container.querySelector(":scope > .main-column, :scope > .revista-main, :scope > .article-main")
            : container;
        if (!target) return;
        const slot = document.createElement("aside");
        slot.className = "tdr-ad-slot tdr-ad-slot--automatic";
        slot.dataset.adSlot = hasSidebarLayout ? "article-inline" : "central-billboard";
        slot.setAttribute("aria-label", "Publicidade contextual");
        const heading = target.querySelector(
            ":scope > .seo-collection-header, :scope > .page-header, :scope > header"
        );
        if (heading) heading.insertAdjacentElement("afterend", slot);
        else target.insertAdjacentElement("afterbegin", slot);
    }

    function loadConfig() {
        if (!configPromise) {
            configPromise = fetch(CONFIG_URL, { cache: "no-store" }).then((response) => {
                if (!response.ok) throw new Error("Configuração publicitária indisponível");
                return response.json();
            });
        }
        return configPromise;
    }

    function contextText(context, includeBody = true) {
        return normalize([
            context.category,
            context.title,
            context.modality,
            context.event_type,
            context.program,
            includeBody ? context.body : "",
            ...(Array.isArray(context.tags) ? context.tags : [])
        ].filter(Boolean).join(" "));
    }

    function categoryFromText(text, rules, priority) {
        return priority.find((category) =>
            (rules[category] || []).some((keyword) => text.includes(normalize(keyword)))
        );
    }

    function resolveCategory(context, config) {
        const explicitCategory = normalize(context.ad_category).replace(/[^a-z0-9]+/g, "");
        const explicitAliases = {
            motos: "motos",
            bicicletas: "bicicletas",
            scooters: "scooters",
            eletricos: "eletricos",
            mobilidade: "mobilidade",
            tecnologia: "tecnologia",
            competicoes: "competicoes",
            eventos: "eventos",
            geral: "geral"
        };
        if (explicitAliases[explicitCategory]) return explicitAliases[explicitCategory];
        const rules = config.category_rules || {};
        const priority = ["scooters", "eletricos", "bicicletas", "motos", "mobilidade", "tecnologia", "competicoes", "eventos"];
        const primaryCategory = categoryFromText(contextText(context, false), rules, priority);
        if (primaryCategory) return primaryCategory;
        const bodyCategory = categoryFromText(normalize(context.body), rules, priority);
        if (bodyCategory) return bodyCategory;
        if (context.type === "competition") return "competicoes";
        if (context.type === "event") return "eventos";
        return "geral";
    }

    function isActive(campaign) {
        if (campaign.status !== "active") return false;
        const now = new Date();
        if (campaign.start_at && now < new Date(campaign.start_at)) return false;
        if (campaign.end_at && now > new Date(campaign.end_at)) return false;
        return true;
    }

    function chooseCampaign(config, category, format) {
        const campaigns = (config.campaigns || []).filter((campaign) =>
            isActive(campaign) &&
            (campaign.formats || []).includes(format)
        );
        return campaigns.find((campaign) => (campaign.categories || []).includes(category)) ||
            campaigns.find((campaign) => (campaign.categories || []).includes("geral"));
    }

    function renderCreative(element, campaign, format, category, definition) {
        if (!campaign) {
            element.hidden = true;
            return;
        }
        const image = campaign.image
            ? `<img src="${esc(campaign.image)}" alt="${esc(campaign.image_alt || campaign.title)}" loading="lazy">`
            : "";
        element.hidden = false;
        element.className = `tdr-ad-slot tdr-ad-slot--${esc(format)} tdr-ad-slot--${esc(category)}`;
        element.dataset.adCategory = category;
        element.dataset.adCampaign = campaign.id;
        element.dataset.adFormat = format;
        element.innerHTML = `<a class="tdr-ad" href="${esc(campaign.url || "contato.html#patrocinio")}" aria-label="${esc(campaign.title)}">
            ${image}
            <span class="tdr-ad__content">
                <small>${esc(campaign.label || "Publicidade")}</small>
                <strong>${esc(campaign.title)}</strong>
                <span>${esc(campaign.description || "")}</span>
                <em>${esc(campaign.cta || "Saiba mais")} →</em>
            </span>
            <span class="tdr-ad__format">${esc(definition?.commercial_name || format)} · ${esc(definition?.width || "")}×${esc(definition?.height || "")}</span>
        </a>`;
    }

    async function refresh(root = document, context = currentContext) {
        if (root === document) ensureDefaultSlot(root);
        currentContext = { ...pageContext(), ...currentContext, ...context };
        try {
            const config = await loadConfig();
            const category = resolveCategory(currentContext, config);
            const elements = root.matches?.("[data-ad-slot]")
                ? [root]
                : [...root.querySelectorAll("[data-ad-slot]")];
            elements.forEach((element) => {
                const slot = config.slots?.[element.dataset.adSlot];
                if (!slot) return;
                const elementCategory = element.dataset.adCategoryOverride || category;
                const campaign = chooseCampaign(config, elementCategory, slot.format);
                renderCreative(element, campaign, slot.format, elementCategory, config.formats?.[slot.format]);
            });
            document.documentElement.dataset.adCategory = category;
            return category;
        } catch (error) {
            console.warn(error);
            return "geral";
        }
    }

    function setContext(context) {
        currentContext = { ...context };
        return refresh(document, currentContext);
    }

    loadGoogleAnalytics();
    window.TVAds = { refresh, setContext, resolveCategory: async (context) => resolveCategory(context, await loadConfig()) };
    document.addEventListener("DOMContentLoaded", () => refresh());
})();
