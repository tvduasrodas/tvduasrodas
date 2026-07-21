# Rotina diária fixada — TVDUASRODAS

Versão fixada em 21 de julho de 2026. Esta rotina é obrigatória para o worker e não pode ser reduzida, substituída ou ignorada sem uma nova instrução expressa de Wesley. O portal não é somente competições e eventos.

## Metas editoriais mínimas do dia

Até o encerramento das 20h (horário Eastern), o worker deve entregar:

1. Pelo menos **uma matéria nova para a Revista**, alternando notícias, lançamentos, testes baseados em dados oficiais, dicas, manutenção, segurança, mobilidade urbana, tecnologia, elétricos, scooters, bicicletas e matérias próprias.
2. Pelo menos **um vídeo novo para a TV**, incorporado do YouTube, confiável, não duplicado e classificado na categoria correta.
3. Todas as **atualizações urgentes de competições e eventos** encontradas em fontes oficiais: resultados, classificação, liderança, calendário ou informação de serviço.
4. **SEO, sitemap, publicação, validação pública e Google Search Console** para toda URL nova.

## Grade fixa dos programas da Revista

Os programas funcionam agora como episódios especiais em texto e fotos, estruturados para equivaler a um futuro programa de 45 minutos. A pauta da Revista deve respeitar esta grade sempre que o dia corresponder:

- **Rolê de Rua:** segundas e quintas — mobilidade, vida urbana, personagens, rotas curtas, scooters, motos e bicicletas na cidade.
- **Garage Tech:** quartas — mecânica, manutenção, componentes, ferramentas e tecnologia explicada.
- **Estrada Aberta:** sábados — rotas, turismo, preparação, segurança e histórias de viagem.
- **Electric Zone:** domingos — veículos elétricos, baterias, recarga, eletrônica, infraestrutura e mobilidade limpa.

Cada episódio precisa ter capa horizontal, no mínimo duas imagens internas quando houver material oficial, texto aprofundado, blocos temáticos com marcação equivalente a 45 minutos, fontes oficiais, links internos e campos `program`, `programLabel`, `episodeDuration` e `readingTime`. Em terças e sextas, a pauta permanece livre entre notícia forte, lançamento, teste baseado em dados oficiais, dica ou matéria própria.

Conteúdo fraco, duplicado, rumor ou texto inventado não cumpre a meta. Quando não houver release forte, a matéria diária deve ser uma pauta própria útil e durável, sustentada por fontes técnicas ou oficiais.

## 08h — Radar editorial e notícias

- Ler a memória da execução anterior e rodar `python scripts/check_daily_targets.py`.
- Verificar de forma incremental salas de imprensa brasileiras, fabricantes, Abraciclo, recalls, CBM, CBC e calendários já monitorados.
- Dar prioridade a recall, segurança, lançamento brasileiro, mudança de mercado, evento próximo e resultado urgente.
- Publicar no máximo uma atualização principal nesta janela quando houver novidade forte.
- Não encerrar o dia nem considerar as metas cumpridas apenas porque competições não mudaram.

## 11h — TV e vídeos

- Pesquisar canais oficiais e canais editoriais confiáveis sobre motos, bicicletas, scooters, elétricos, testes, manutenção, mobilidade e competições.
- Publicar um vídeo recente e ainda não cadastrado. Preferir os últimos 30 dias; conteúdo mais antigo só quando for especialmente útil e atual.
- Confirmar título, canal, disponibilidade do embed e ID do YouTube.
- Escrever título e descrição originais em português brasileiro e informar quando o vídeo for externo ou estiver em outro idioma.
- Categorizar corretamente: Competições, Motocross/Cross, Urbano, Lançamentos, Testes e Avaliações, Dicas e Manutenção, Tecnologia e Elétricos, Bicicletas/BMX, Eventos ou Cassetadas/Entretenimento.
- Atualizar o sitemap e publicar. Se nenhum vídeo adequado for encontrado, registrar as fontes tentadas e deixar a meta pendente para as 20h.

## 14h — Revista e matéria própria

- Rodar `python scripts/check_daily_targets.py` e verificar se já existe matéria publicada no dia.
- Se não existir, produzir obrigatoriamente a matéria diária.
- Quando não houver notícia ou lançamento forte, usar pauta própria durável: segurança, manutenção, pilotagem, compra, documentação, viagem, mobilidade, urbanização, tecnologia, bicicletas, scooters ou elétricos.
- Usar texto original em pt-BR, sem copiar releases e sem afirmar teste presencial que não ocorreu.
- Priorizar capa oficial horizontal e duas imagens internas autorizadas. Baixar, otimizar e publicar localmente; não usar hotlink. IA somente quando não houver material oficial adequado.
- Registrar fontes, direitos, créditos e tratamento das imagens.

## 17h — Competições, eventos e segunda rodada de notícias

- Verificar resultados, pódios, pontos, liderança, etapas, calendários e documentos oficiais publicados desde a última checagem.
- Atualizar páginas existentes e preservar histórico; não publicar apenas o vencedor quando a tabela oficial completa estiver disponível.
- Verificar eventos nacionais e internacionais relevantes ao público brasileiro.
- Se não houver mudança esportiva, procurar notícia relevante de produto, mercado, recall, segurança, mobilidade ou ciclismo. A janela não termina apenas com “sem novidade em competições”.

## 20h — Fechamento obrigatório, SEO e indexação

- Rodar `python scripts/check_daily_targets.py --require-complete`.
- Se faltar matéria ou vídeo, produzir e publicar o item pendente antes de encerrar, respeitando qualidade, fontes e direitos.
- Revisar URLs novas e materialmente alteradas do dia.
- Executar a lista de SEO e confirmar o site público.
- Enviar o sitemap atualizado ao Google Search Console e solicitar indexação das novas páginas, sempre usando `tvduasrodas@gmail.com`.
- Publicar um relatório visível com entregas, URLs, fontes, SEO/Search Console e qualquer bloqueio real.

## Lista obrigatória para cada nova página ou URL

1. Verificar duplicidade e criar slug curto, descritivo e preferencialmente sem acentos.
2. Validar título SEO, meta description, canonical, Open Graph/Twitter, imagem social, texto alternativo, links internos e schema pertinente.
3. Comprimir imagens e confirmar capa e imagens internas carregando.
4. Executar `python scripts/update_sitemap.py`.
5. Validar XML, URLs únicas e ausência de fragmentos inválidos como `#U` ou `%23U`.
6. Fazer commit apenas dos arquivos relacionados e push para `origin/main`.
7. Confirmar a URL, imagem, layout e sitemap no domínio público.
8. No Google Search Console, entrar somente como `tvduasrodas@gmail.com`, reenviar `https://tvduasrodas.com/sitemap.xml` após o lote publicado e solicitar indexação das URLs novas. Nunca usar `wesleyrodrigo29@gmail.com`.

## Regras permanentes

- Repositório único: `C:\Users\Wesley\Documents\TVDUASRODAS\tvduasrodas`, branch `main`.
- Nunca alterar ou publicar no projeto `itservices` nem no clone antigo do GitHub Desktop.
- Priorizar fontes oficiais, imagens de imprensa licenciadas e créditos corretos.
- Não deixar publicação válida somente no computador: validar, fazer commit, push e confirmar no site.
- Toda execução gera relatório visível: checado sem novidade, publicado com URL ou ação necessária.
- CAPTCHA, 2FA, novo OAuth, pagamento ou nova permissão exigem Wesley; tarefas independentes continuam.
