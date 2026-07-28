# Política de indexação de eventos

As páginas de eventos da TVDUASRODAS são permanentes.

- Um evento encerrado não deve ser apagado, redirecionado para a agenda nem receber `noindex`.
- A URL canônica original permanece respondendo com HTML completo e código HTTP 200.
- Todos os eventos, futuros e passados, permanecem no `sitemap.xml` e no `event-sitemap.xml`.
- Depois da data, o JSON-LD muda para `EventCompleted` e ofertas ativas deixam de ser publicadas.
- A página encerrada deve continuar apta a receber resultados, fotos, vídeos, classificação e cobertura posterior.
- O `lastmod` só muda quando houver atualização material do conteúdo, dos dados estruturados ou dos links.
- Eventos próximos são priorizados na monitoração por data, mas a inspeção não garante indexação imediata.
- A Google Indexing API não deve ser usada para eventos presenciais comuns; ela é reservada pelo Google a `JobPosting` e `BroadcastEvent` incorporado a `VideoObject`.

O fluxo automático envia três sitemaps ao Search Console:

1. `sitemap.xml`, com todas as URLs canônicas;
2. `news-sitemap.xml`, somente com matérias das últimas 48 horas;
3. `event-sitemap.xml`, com todas as páginas permanentes de eventos.

O painel de status inspeciona as matérias recentes e os eventos em andamento ou mais próximos. O envio do painel ao GitHub usa rebase e novas tentativas para não falhar quando outra publicação avança a branch principal.
