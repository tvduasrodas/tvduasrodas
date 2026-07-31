#!/usr/bin/env python3
"""Consolida duplicatas confirmadas sem perder as rotas públicas antigas."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"

# Pares revisados manualmente: alias/erro de digitação -> registro canônico.
CONFIRMED_ALIASES = {
    "aguais-da-liberdade-mc-conselheiro-lafaiete-mg-2026-07-25":
        "aguias-da-liberdade-mc-conselheiro-lafaiete-mg-2026-07-25",
    "karangos-e-motocas-mc-duque-de-caxias-mg-2026-07-26":
        "karangos-e-motocas-mc-duque-de-caxias-rj-2026-07-26",
    "7-encontro-de-moticiclistas-e-triciclistas-oliveira-fortes-mg-2026-07-31":
        "7-encontro-de-motociclistas-e-triciclistas-oliveira-fortes-mg-2026-07-31",
    "7-encontro-de-motociclistas-oliveira-fortes-mg-2026-07-31":
        "7-encontro-de-motociclistas-e-triciclistas-oliveira-fortes-mg-2026-07-31",
    "guardioes-de-raul-mc-sumidouro-rj-2026-07-31":
        "guardioes-do-raul-mc-sumidouro-rj-2026-07-31",
    "2-encontro-de-motocicilstas-lavras-novas-mg-2026-08-01":
        "2-encontro-de-motociclistas-lavras-novas-mg-2026-08-01",
    "motofest-simonesia-go-2026-08-07":
        "motofest-simonesia-mg-2026-08-07",
    "moto-festival-pocos-de-caldas-mg-2026-08-07":
        "ii-moto-festival-pocos-de-caldas-mg-2026-08-07",
    "cavaleiros-sem-rumo-campos-dos-goytacazes-rj-2026-08-15":
        "cavaleiros-sem-rumo-mc-campos-dos-goytacazes-rj-2026-08-15",
    "garras-sobre-rodas-rio-de-janeiro-rj-2026-08-15":
        "garras-sobre-rodas-mc-rio-de-janeiro-rj-2026-08-15",
    "aguais-de-cristo-mc-belo-horizonte-mg-2026-08-15":
        "aguias-de-cristo-mc-belo-horizonte-mg-2026-08-15",
    "rat-bike-brasil-jeceaba-mg-2026-08-15":
        "12-acampamento-nacional-rat-bike-do-brasil-jeceaba-mg-2026-08-15",
    "rock-chopper-mc-saquarema-rj-2026-08-15":
        "5-praia-rock-chopper-mc-saquarema-rj-2026-08-15",
    "jaguar-negro-mc-the-steel-skulls-mc-belo-horizonte-mg-2026-08-08":
        "jaguar-negro-mc-e-the-steel-skulls-mc-belo-horizonte-mg-2026-08-08",
    "mundicas-o-chamado-da-estrada-nova-pauliceia-sp-2026-08-09":
        "mundicas-mg-o-chamado-da-estrada-nova-pauliceia-gaviao-peixoto-sp-2026-08-09",
    "autoridade-mc-uboranga-mg-2026-09-04":
        "autoridade-mc-ubaporanga-mg-2026-09-04",
    "encontro-de-motociclistas-iguaba-grande-rj-2026-09-04":
        "motofest-iguaba-grande-rj-2026-09-04",
    "motocafe-santopolis-do-aguapei-sp-2026-09-20":
        "moto-cafe-santopolis-do-aguapei-sp-2026-09-20",
    "motorock-uru-sp-2026-10-30":
        "4-festival-da-pimenta-e-motorock-uru-sp-2026-10-30",
    "9-encontro-de-motociclistas-e-triciclistas-lutecia-sp-2026-11-07":
        "9-encontro-de-motociclistas-e-triciclistas-lutecia-sp-2026-11-06",
    "motofest-lagoinha-sao-jose-do-rio-preto-sp-2026-11-21":
        "moto-fest-lagoinha-sao-jose-do-rio-preto-sp-2026-11-21",
    "motofest-prog-manhumirim-mg-2026-07-31":
        "motofest-manhumirim-mg-2026-07-31",
    "amigos-na-estrada-mc-sao-jose-do-vale-rio-preto-rj-2026-08-23":
        "amigos-na-estrada-mc-sao-jose-do-vale-do-rio-preto-rj-2026-08-23",
    "os-mutantes-mc-e-road-rhino-mc-rio-de-janeiro-rj-2026-09-13":
        "mc-os-mamutes-e-road-rhino-mc-rio-de-janeiro-rj-2026-09-13",
    "classicos-estraderios-mg-rio-de-janeiro-rj-2026-10-11":
        "classicos-estradeiros-mg-rio-de-janeiro-rj-2026-10-11",
    "classics-estradeiros-mg-rio-de-janeiro-rj-2026-10-11":
        "classicos-estradeiros-mg-rio-de-janeiro-rj-2026-10-11",
    "7-encontro-nacional-fama-mg-2026-09-11":
        "7-encontro-nacional-de-motociclistas-fama-mg-2026-09-11",
    "tiao-e-deja-pirassununga-sp-2026-09-25":
        "tiao-e-deja-moto-casal-pirassununga-sp-2026-09-25",
    "mc-ponta-negra-marica-rj-2026-10-31":
        "7-aniversario-mc-ponta-negra-marica-rj-2026-10-31",
    "14-encontro-nacional-de-motociclistas-sao-joao-del-rei-mg-2026-07-23":
        "14-encontro-nacional-sao-joao-del-rei-mg-2026-07-23",
    "14-encontro-nacional-de-motociclistas-sao-joao-del-rei-mg-2026-07-24":
        "14-encontro-nacional-sao-joao-del-rei-mg-2026-07-23",
    "4-encotnro-nacional-de-motociclistas-ouro-preto-mg-2026-07-24":
        "4-encontro-nacional-de-motociclistas-ouro-preto-mg-2026-07-24",
    "4-motofest-divinopolis-mg-2026-07-24":
        "divina-motofest-divinopolis-mg-2026-07-24",
    "mc-campos-compos-dos-goytacazes-rj-2026-07-24":
        "mc-campos-campos-dos-goytacazes-rj-2026-07-24",
    "moto-rock-festival-baependi-mg-2026-07-24":
        "moto-rock-festival-de-inverno-baependi-mg-2026-07-24",
    "piratas-de-aco-mc-100-censura-rio-claro-sp-2026-07-24":
        "piratas-de-aco-mc-e-100-censura-rio-claro-sp-2026-07-24",
    "bike-fest-poa-sp-2026-07-25":
        "2-bike-fest-poa-sp-2026-07-25",
    "pererecas-mc-belford-roxo-rio-de-janeiro-rj-2026-07-25":
        "pererecas-mc-belford-roxo-rj-2026-07-25",
    "motofest-iguatu-pr-2026-07-30":
        "motofest-iguatu-ce-2026-07-30",
    "motofest-extrema-mg-2026-07-31":
        "14-motofest-extrema-mg-2026-07-31",
    "motofest-serra-es-2026-07-31":
        "7-serra-moto-fest-serra-es-2026-07-31",
    "motofest-blumenau-sc-2026-07-31":
        "moto-festival-blumenau-sc-2026-07-31",
    "motofest-delmiro-al-2026-07-31":
        "motofest-delmiro-gouveia-al-2026-07-31",
    "irmaos-das-sombras-mc-senador-vasconcelos-rio-de-janerio-rj-2026-08-01":
        "irmaos-das-sombras-mc-senador-vasconcelos-rio-de-janeiro-rj-2026-08-01",
    "ilha-mc-ilha-do-governador-rio-de-janeiro-rj-2026-08-15":
        "ilha-mc-ilha-do-governador-rj-2026-08-15",
    "impreriais-mc-cachoeiras-de-macacu-rj-2026-08-15":
        "imperiais-mc-cachoeiras-de-macacu-rj-2026-08-15",
    "espirito-de-agua-mc-contagem-mg-2026-08-22":
        "espirito-de-aguia-mc-contagem-mg-2026-08-22",
    "encontro-nacional-de-motociclistas-ijaci-mg-2026-08-28":
        "encontro-nacional-de-motociclistas-e-triciclistas-ijaci-mg-2026-08-28",
    "v-encontro-nacional-ijaci-mg-2026-08-28":
        "encontro-nacional-de-motociclistas-e-triciclistas-ijaci-mg-2026-08-28",
    "moto-fest-senador-amaral-mg-2026-08-28":
        "motofest-senador-amaral-mg-2026-08-28",
    "trike-brasil-mc-prog-minduri-mg-2026-08-28":
        "trike-brasil-mc-minduri-mg-2026-08-28",
    "old-pistons-ms-volta-redonda-rj-2026-09-12":
        "old-pistons-volta-redonda-rj-2026-09-12",
    "nostalgia-mc-caes-de-zorba-mc-santa-barbara-d-oeste-sp-2026-09-18":
        "nostalgia-mc-e-caes-de-zorba-mc-santa-barbara-d-oeste-sp-2026-09-18",
    "moto-cafe-paraguacu-paulista-sp-2026-09-20":
        "2-moto-cafe-paraguacu-paulista-sp-2026-09-20",
    "motofest-resende-rj-2026-09-20":
        "4-motofest-resende-rj-2026-09-20",
    "dragoes-da-alvorada-mg-santa-terezinha-do-itaipu-pr-2026-11-28":
        "dragoes-da-alvorada-mg-santa-terezinha-de-itaipu-pr-2026-11-28",
}


def main() -> None:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    entries = document.get("entries", [])
    by_slug = {entry.get("slug"): entry for entry in entries}
    missing = {
        slug
        for pair in CONFIRMED_ALIASES.items()
        for slug in pair
        if slug not in by_slug
    }
    if missing:
        raise SystemExit(f"Slugs não encontrados: {sorted(missing)}")

    changed = 0
    for alias, canonical in CONFIRMED_ALIASES.items():
        entry = by_slug[alias]
        canonical_entry = by_slug[canonical]
        if canonical_entry.get("duplicate_of") == alias:
            canonical_entry.pop("duplicate_of", None)
            canonical_entry.pop("canonical_url", None)
        canonical_sources = canonical_entry.setdefault("sources", [])
        known_urls = {
            source.get("url") for source in canonical_sources
            if isinstance(source, dict)
        }
        for source in entry.get("sources", []):
            if isinstance(source, dict) and source.get("url") not in known_urls:
                canonical_sources.append(source)
                known_urls.add(source.get("url"))
        if entry.get("duplicate_of") != canonical:
            entry["duplicate_of"] = canonical
            entry["canonical_url"] = f"/eventos/{canonical}/"
            entry["last_updated"] = "2026-07-26"
            changed += 1

    # O nome do bairro foi importado como cidade nesta variação do flyer.
    mundicas = by_slug[
        "mundicas-mg-o-chamado-da-estrada-nova-pauliceia-gaviao-peixoto-sp-2026-08-09"
    ]
    mundicas["city"] = "Gavião Peixoto"
    mundicas["venue"] = "Nova Pauliceia"
    mundicas["state"] = "SP"

    # A variação "prog" de Manhumirim recebeu primeiro a leitura completa do
    # flyer; transfere esses fatos para a URL pública principal.
    manhumirim_alias = by_slug["motofest-prog-manhumirim-mg-2026-07-31"]
    manhumirim = by_slug["motofest-manhumirim-mg-2026-07-31"]
    for field in (
        "title", "short_name", "end_date", "venue", "street_address",
        "full_address", "time_label", "organizer", "admission_status",
        "attractions", "summary", "body", "contact", "services",
        "visual_verification",
    ):
        if manhumirim_alias.get(field):
            manhumirim[field] = manhumirim_alias[field]

    AGENDA.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Duplicatas canônicas atualizadas: {changed}")


if __name__ == "__main__":
    main()
