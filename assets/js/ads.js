(function () {
    "use strict";

    const CONFIG_URL = "content/ads/config.json";
    let configPromise;
    let currentContext = {};

    const normalize = (value) => String(value || "")
        .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        .toLowerCase();

    const esc = (value) => String(value ?? "")
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;").replace(/'/g, "&#39;");

    function loadConfig() {
        if (!configPromise) {
            configPromise = fetch(CONFIG_URL, { cache: "no-store" }).then((response) => {
                if (!response.ok) throw new Error("Configuração publicitária indisponível");
                return response.json();
            });
        }
        return configPromise;
    }

    function contextText(context) {
        return normalize([
            context.category,
            context.title,
            context.modality,
            context.event_type,
            context.program,
            context.body,
            ...(Array.isArray(context.tags) ? context.tags : [])
        ].filter(Boolean).join(" "));
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
        const text = contextText(context);
        const rules = config.category_rules || {};
        const priority = ["scooters", "eletricos", "bicicletas", "motos", "mobilidade", "tecnologia", "competicoes", "eventos"];
        for (const category of priority) {
            if ((rules[category] || []).some((keyword) => text.includes(normalize(keyword)))) {
                return category;
            }
        }
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
        currentContext = { ...currentContext, ...context };
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

    window.TVAds = { refresh, setContext, resolveCategory: async (context) => resolveCategory(context, await loadConfig()) };
    document.addEventListener("DOMContentLoaded", () => refresh());
})();
