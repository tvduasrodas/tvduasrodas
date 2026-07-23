# Rotina diária fixada — TVDUASRODAS

Versão atualizada em 23 de julho de 2026. Esta rotina é obrigatória para o worker e não pode ser reduzida, substituída ou ignorada sem uma nova instrução expressa de Wesley. O portal não é somente competições e eventos.

## Sincronização obrigatória entre este arquivo e as automações

- Este arquivo é a fonte principal e soberana das regras de todas as automações da TVDUASRODAS.
- Todas as regras universais deste arquivo se aplicam a todas as automações atuais e futuras do projeto e a cada ocorrência programada, sem diferença de rigor entre horários.
- Sempre que qualquer configuração, prompt, horário, escopo, formato, ferramenta, recuperação ou regra de uma automação for criada ou alterada, a mesma mudança deve ser registrada neste arquivo durante a mesma execução.
- Uma alteração de automação não pode ser considerada concluída enquanto este arquivo não estiver sincronizado, validado, incluído em commit e publicado em `origin/main`.
- Se existir diferença entre a configuração de uma automação e este arquivo, interromper o encerramento, corrigir a divergência e aplicar a recuperação obrigatória de publicação.
- O relatório da alteração deve confirmar explicitamente: `configuração da automação atualizada`, `ROTINA-DIARIA-AUTOMACAO.md sincronizado`, `commit publicado` e `origin/main confirmado`.

## Isolamento obrigatório de cada janela automatizada

- Cada ocorrência de qualquer automação — horários editoriais às **08h, 11h, 14h, 17h e 20h** e horários do Instagram às **08h30, 11h30, 14h30, 17h30 e 20h30**, em `America/New_York` — deve iniciar em uma **nova tarefa independente do Codex**. É proibido continuar qualquer execução automática em uma tarefa usada por outra ocorrência, mesmo quando pertencer à mesma automação.
- A primeira ação da nova tarefa deve ser abrir e ler **integralmente** `C:\Users\Wesley\Documents\TVDUASRODAS\tvduasrodas\ROTINA-DIARIA-AUTOMACAO.md`. Nenhuma pesquisa, diagnóstico, seleção de pauta, edição, publicação ou uso da memória pode ocorrer antes dessa leitura.
- Nenhum skill, memória, navegador, pesquisa, diagnóstico, arquivo auxiliar ou outra ferramenta pode ser consultado antes da leitura integral deste documento.
- Depois da leitura, este arquivo deve ser tratado como **autoridade operacional absoluta** para toda a janela. Conversas anteriores, resumos e memória são apenas contexto e nunca podem reduzir, substituir, reinterpretar ou adiar uma regra obrigatória daqui.
- A memória da automação pode ser consultada somente **depois** da leitura integral deste arquivo e serve para continuidade factual e prevenção de duplicidade, não para transportar o peso ou o raciocínio da tarefa anterior.
- Se a execução perceber que não está em uma tarefa nova e independente, deve interromper o trabalho nessa tarefa e iniciar uma nova tarefa antes de prosseguir. Não é permitido compensar essa falha resumindo ou limpando a conversa existente.
- A execução deve declarar no primeiro resumo interno da janela: `nova tarefa confirmada`, `ROTINA-DIARIA-AUTOMACAO.md lida integralmente`, data, dia da semana e horário calculados em Eastern.

## Particionamento das automações e aplicação das regras

Existem duas automações ativas vinculadas ao projeto `TVDUASRODAS`, e não uma configuração separada para cada horário:

1. `Atualizações otimizadas TV Duas Rodas`: uma única configuração executada às **08h, 11h, 14h, 17h e 20h**. O horário determina qual janela editorial deste documento deve ser executada; todas as regras universais, especialmente leitura inicial, isolamento, qualidade, validação, commit, push, recuperação, Search Console e relatório, valem igualmente nas cinco ocorrências.
2. `Instagram TVDUASRODAS — Reels e Stories`: uma única configuração executada às **08h30, 11h30, 14h30, 17h30 e 20h30**. Todas as regras universais valem igualmente nas cinco ocorrências, acrescidas das regras específicas da seção **Instagram — somente Reels e Stories**.

- É proibido criar versões de regras diferentes por horário dentro da mesma automação. Uma regra universal adicionada ou alterada deve ser aplicada à configuração completa e, portanto, a todas as ocorrências daquela automação.
- Diferenças entre horários podem existir somente no trabalho editorial específico descrito nas seções 08h, 11h, 14h, 17h e 20h, nunca nas regras de leitura obrigatória, isolamento, autorização, commit, push, recuperação ou confirmação remota.
- Se uma nova automação for criada para este projeto, ela deve ser adicionada a esta seção e receber integralmente o bloco universal de leitura, isolamento, publicação e recuperação antes de ser ativada.

## Metas editoriais mínimas do dia

Antes de escolher ou classificar qualquer pauta, calcular novamente a data e o dia da semana em `America/New_York`. Não reutilizar o dia da semana registrado por uma execução anterior. Declarar no resumo da janela o dia calculado e o programa correspondente. Se uma urgência editorial substituir a grade fixa, registrar explicitamente a exceção e o motivo.

Até o encerramento das 20h (horário Eastern), o worker deve entregar:

1. Pelo menos **uma matéria nova e independente para a Revista**, com `contentType: "article"`. Matéria própria, notícia e edição de programa são tipos diferentes; notícia e programa não substituem esta meta.
2. Nos dias da grade fixa, **uma nova edição do programa correspondente**, com `contentType: "program"`, além da matéria diária. A edição deve ser identificada como a edição daquela semana e nunca pode ser contada como matéria diária.
3. Pelo menos **um vídeo novo para a TV com áudio em português brasileiro**, incorporado do YouTube, confiável, não duplicado e classificado na categoria correta. Vídeo em inglês, espanhol ou outro idioma não cumpre a meta, mesmo quando título e descrição estiverem traduzidos.
4. Diversificar a TV durante a semana: não repetir categoria de vídeo nem canal de origem na mesma semana editorial, salvo transmissão ou atualização oficial urgente, com exceção explicada no relatório. Alternar testes, competições, cross, eventos, urbano, lançamentos, dicas, tecnologia, viagem, história, customização, entretenimento e outras categorias pertinentes.
5. Todas as **atualizações urgentes de competições e eventos** encontradas em fontes oficiais: resultados, classificação, liderança, calendário ou informação de serviço.
6. **SEO, sitemap, publicação, validação pública e Google Search Console imediatamente após cada lote publicado**, sem esperar o fechamento das 20h.

### Rotação semanal de matérias

- Toda matéria própria deve usar `contentType: "article"` e uma categoria ainda não usada por outra matéria própria na mesma semana, de segunda a domingo.
- Se uma matéria própria da categoria Cross já foi publicada naquela semana, a próxima matéria própria deve usar outra categoria.
- Notícias factuais usam `contentType: "news"` e podem repetir categoria quando houver novidade real, desdobramento ou atualização verificável.
- Edições de programa usam `contentType: "program"` e não participam da contagem da matéria diária nem da rotação de categorias das matérias próprias.
- Notícia cujo conteúdo principal seja agenda, serviço ou programação deve ir para Eventos. Resultado, classificação, etapa, liderança ou calendário esportivo deve atualizar Competições. Só publicar também na Revista quando existir uma reportagem editorial própria, com contexto e valor além da atualização estrutural.

## SEO imediato após cada publicação

Toda criação ou alteração pública deve encerrar o próprio ciclo de SEO antes de a execução seguir para outra pauta. Não esperar 20h.

1. Preparar SEO completo e executar `python scripts/update_sitemap.py` e `python scripts/update_sitemap.py --check`.
2. Fazer commit e push do lote.
3. Confirmar no domínio público a página alterada e o sitemap publicado.
4. Reenviar `https://tvduasrodas.com/sitemap.xml` no Google Search Console usando somente `tvduasrodas@gmail.com`.
5. Para cada URL nova, solicitar indexação imediatamente após a publicação pública.
6. Registrar os estados corretos: `sitemap reenviado`, `indexação solicitada`, `indexada` ou `pendente`. Nunca chamar uma solicitação de indexação concluída.
7. Se push, acesso público ou Search Console falhar, registrar a pendência e aplicar a recuperação prevista neste documento; não adiar silenciosamente até 20h.

A auditoria das 20h é uma camada adicional de segurança para localizar qualquer SEO pendente do dia. Ela não substitui o SEO imediato de cada lote.

## Instagram — somente Reels e Stories

- A automação `Instagram TVDUASRODAS — Reels e Stories` executa diariamente às **08h30, 11h30, 14h30, 17h30 e 20h30**, em `America/New_York`, depois das janelas editoriais principais.
- Cada conteúdo novo elegível do portal deve gerar somente **um Reel** e **um Story** coordenados, sem duplicação.
- É proibido criar, agendar ou publicar posts de Feed, fotografias no grid ou carrosséis. A opção `Create post` do Meta Business Suite não deve ser usada.
- O Feed existente deve ser preservado. Não excluir publicações antigas. Registros antigos com Feed são apenas histórico e não autorizam repetição.
- Para novos registros em `output/instagram/publication-log.json`, omitir o campo de Feed ou registrar `NAO_APLICAVEL_POR_REGRA`, sem gerar arquivo ou publicação para o Feed.
- Stories devem usar formato vertical `1080x1920`, vídeo MP4 de 12 a 15 segundos, H.264 com áudio AAC e trilha original ou comprovadamente licenciada.
- Reels devem usar formato vertical `1080x1920`, MP4 H.264 com áudio AAC, preferencialmente entre 20 e 35 segundos, gancho nos primeiros dois segundos, 4 a 7 cenas, textos dentro da área segura, capa legível e CTA para seguir `@tvduasrodasofc` e acessar `TVDUASRODAS.COM`.
- Não usar música comercial sem licença, não fabricar cenas documentais e não afirmar publicação sem confirmação visível na conta profissional `@tvduasrodasofc`.
- Usar obrigatoriamente `Create reel` para Reels e `Create story` para Stories. Nunca publicar o vídeo como post comum.
- Registrar separadamente, para cada Story e Reel: arquivo, duração, trilha, horário, destino, permalink ou identificador disponível e confirmação verdadeira da publicação.
- Todos os arquivos e registros criados pela automação do Instagram devem ser incluídos em commit e push para `origin/main` antes do encerramento. Se o push direto falhar, aplicar imediatamente a seção **Recuperação obrigatória de publicação** deste documento.
- A automação do Instagram não pode declarar conclusão com arquivos apenas locais, commit à frente de `origin/main` ou publicação sem confirmação.

## Grade fixa dos programas da Revista

Os programas funcionam como edições especiais em texto e fotos, publicadas separadamente da matéria diária. A grade deve ser cumprida sempre que o dia corresponder:

- **Rolê de Rua:** segundas e quintas — mobilidade, vida urbana, personagens, rotas curtas, scooters, motos e bicicletas na cidade.
- **Garage Tech:** quartas — mecânica, manutenção, componentes, ferramentas e tecnologia explicada.
- **Estrada Aberta:** sábados — rotas, turismo, preparação, segurança e histórias de viagem.
- **Electric Zone:** domingos — veículos elétricos, baterias, recarga, eletrônica, infraestrutura e mobilidade limpa.

Cada edição precisa ter `contentType: "program"`, capa horizontal, no mínimo duas imagens internas quando houver material oficial, texto aprofundado, fontes oficiais, links internos e campos `program`, `programLabel`, `episodeDuration` e `readingTime`. O título deve identificar a edição da semana de forma editorial, por exemplo `Rolê de Rua — edição de DD/MM/AAAA`, sem transformar essa identificação em texto burocrático. A duração planejada e qualquer estrutura de futuro programa em vídeo são informações internas: nunca publicar ao leitor marcações de minutos, bastidores ou avisos sobre um futuro TV Show. Em terças e sextas não há edição fixa, mas a matéria diária independente continua obrigatória.

Conteúdo fraco, duplicado, rumor ou texto inventado não cumpre a meta. Quando não houver release forte, a matéria diária deve ser uma pauta própria útil e durável, sustentada por fontes técnicas ou oficiais.

## 08h — Radar editorial e notícias

- Ler a memória da execução anterior e rodar `python scripts/check_daily_targets.py`.
- Fazer a **primeira verificação obrigatória de SEO do dia** com `python scripts/update_sitemap.py --check`.
- Conferir se o fechamento de SEO do dia anterior foi concluído: sitemap gerado depois da última publicação, enviado ao Google Search Console e URLs novas solicitadas para indexação. Se faltar qualquer etapa, corrigir, publicar e concluir usando somente `tvduasrodas@gmail.com` antes de seguir.
- Se o sitemap estiver desatualizado, executar `python scripts/update_sitemap.py`, validar a contagem por coleção, publicar e reenviar o sitemap no Search Console.
- Verificar de forma incremental salas de imprensa brasileiras, fabricantes, Abraciclo, recalls, CBM, CBC e calendários já monitorados.
- Dar prioridade a recall, segurança, lançamento brasileiro, mudança de mercado, evento próximo e resultado urgente.
- Publicar no máximo uma atualização principal nesta janela quando houver novidade forte.
- Não encerrar o dia nem considerar as metas cumpridas apenas porque competições não mudaram.

## 11h — TV e vídeos

- Pesquisar canais oficiais e canais editoriais confiáveis sobre motos, bicicletas, scooters, elétricos, testes, manutenção, mobilidade e competições.
- Antes da escolha, revisar os vídeos publicados desde a segunda-feira e eliminar canais e categorias já usados na semana.
- Publicar um vídeo recente e ainda não cadastrado, obrigatoriamente com áudio em português brasileiro. Preferir os últimos 30 dias; conteúdo mais antigo só quando for especialmente útil e atual.
- Confirmar título, canal, idioma do áudio, disponibilidade do embed e ID do YouTube. Registrar `channel` e `language: "pt-BR"` no frontmatter.
- Escrever título e descrição originais em português brasileiro. Legenda ou descrição traduzida não torna elegível um vídeo cujo áudio esteja em outro idioma.
- Não concentrar a seleção em reviews nem usar o mesmo canal em dias seguidos ou mais de uma vez na semana. Um canal externo pode reaparecer em outra semana, preservando diversidade editorial.
- Categorizar corretamente: Competições, Motocross/Cross, Urbano, Lançamentos, Testes e Avaliações, Dicas e Manutenção, Tecnologia e Elétricos, Bicicletas/BMX, Eventos ou Cassetadas/Entretenimento.
- Atualizar o sitemap, publicar e concluir imediatamente o ciclo de SEO e Search Console. Se nenhum vídeo adequado em pt-BR for encontrado, registrar canais e categorias tentados e deixar a meta pendente para as 20h; não preencher a meta com vídeo estrangeiro.

## 14h — Revista e matéria própria

- Rodar `python scripts/check_daily_targets.py` e verificar separadamente matéria diária, vídeo e programa da grade.
- Se não existir `contentType: "article"`, produzir obrigatoriamente a matéria diária, mesmo que já exista notícia ou edição de programa no dia.
- Conferir as categorias das matérias próprias publicadas desde segunda-feira e escolher uma categoria ainda não usada na semana.
- Quando houver programa fixo no dia, produzir também uma edição separada com `contentType: "program"`. O programa não substitui a matéria diária e a matéria diária não substitui o programa.
- Quando não houver notícia ou lançamento forte, usar pauta própria durável: segurança, manutenção, pilotagem, compra, documentação, viagem, mobilidade, urbanização, tecnologia, bicicletas, scooters ou elétricos.
- Usar texto original em pt-BR, sem copiar releases e sem afirmar teste presencial que não ocorreu.
- Priorizar capa oficial horizontal e duas imagens internas autorizadas. Baixar, otimizar e publicar localmente; não usar hotlink. IA somente quando não houver material oficial adequado.
- Registrar fontes, direitos, créditos e tratamento das imagens.
- Após cada lote publicado, concluir imediatamente sitemap, push, validação pública e Search Console.

## 17h — Competições, eventos e segunda rodada de notícias

- Verificar resultados, pódios, pontos, liderança, etapas, calendários e documentos oficiais publicados desde a última checagem.
- Atualizar páginas existentes e preservar histórico; não publicar apenas o vencedor quando a tabela oficial completa estiver disponível.
- Verificar eventos nacionais e internacionais relevantes ao público brasileiro.
- Se não houver mudança esportiva, procurar notícia relevante de produto, mercado, recall, segurança, mobilidade ou ciclismo. A janela não termina apenas com “sem novidade em competições”.

## 20h — Fechamento obrigatório e auditoria final de SEO

- Rodar `python scripts/check_daily_targets.py --require-complete`.
- Se faltar matéria independente, vídeo elegível em pt-BR ou programa fixo do dia, produzir e publicar cada item pendente antes de encerrar, respeitando qualidade, fontes, diversidade e direitos.
- Revisar URLs novas e materialmente alteradas do dia.
- Fazer a **auditoria final obrigatória de SEO do dia**. Verificar se cada push público já teve sitemap reenviado e, para cada URL nova, indexação solicitada imediatamente após a publicação. Corrigir qualquer lacuna encontrada.
- Se não houve mudança no site, ainda assim executar `python scripts/update_sitemap.py --check` e registrar a validação no relatório.
- Quando houve atualização, confirmar no Search Console o estado de **todas** as URLs novas e reenviar o sitemap se necessário, sempre usando `tvduasrodas@gmail.com`. Esta conferência é redundância de segurança, não o primeiro envio do dia.
- Depois da última atualização, publicar o relatório diário consolidado descrito abaixo. O relatório deve cobrir o dia inteiro, e não apenas a execução das 20h.

## Relatório diário consolidado — depois da última atualização

Na execução das 20h, depois de publicar, validar e indexar o último lote do dia, o worker deve enviar a Wesley um relatório visível em português brasileiro com tudo o que foi feito desde 00h no horário Eastern.

Usar sempre o formato compacto abaixo, com um parágrafo por categoria e links clicáveis nos títulos publicados:

```text
Relatório de hoje — DD/MM/AAAA
**Revista:** matérias independentes e notícias do dia, separadas por tipo, com título, categoria e URL.
**TV:** vídeos incluídos, com título, URL, categoria, canal e confirmação de áudio em pt-BR.
**Competições:** resultados, classificações, lideranças e campeonatos cadastrados ou atualizados.
**Eventos:** eventos e informações de serviço adicionados ou atualizados.
**Calendário:** alterações de datas, etapas e agenda.
**Revista/programas:** edições de programas publicadas separadamente das matérias, com programa, edição e URL.
**Imagens e desempenho:** capas, compressão, cache e correções visuais relevantes.
**SEO:** ciclos concluídos após cada push, sitemap, total de URLs e auditoria das 20h.
**Google Search Console:** horário de cada reenvio do sitemap e estado de cada solicitação de indexação.
**Pendências:** bloqueios, autenticações ou aprovações; se não houver, informar isso claramente.
A rotina continua às **08h, 11h, 14h, 17h e 20h**, com o relatório completo enviado após a execução das 20h.
```

Quando uma categoria não tiver mudança, escrever `sem atualização no dia` em vez de omiti-la. O relatório deve ser objetivo como o modelo, mas incluir todos os itens efetivamente publicados ou alterados no dia.

Para montar o relatório, conferir o histórico de publicações e alterações do dia inteiro. Não contar simples correções de cache como novas matérias. Não afirmar que o Google indexou uma página quando houve apenas solicitação; usar os estados corretos, como `sitemap processado`, `indexação solicitada` ou `indexada`, conforme a confirmação visível.

## Lista obrigatória para cada nova página ou URL

1. Verificar duplicidade e criar slug curto, descritivo e preferencialmente sem acentos.
2. Validar título SEO, meta description, canonical, Open Graph/Twitter, imagem social, texto alternativo, links internos e schema pertinente.
3. Comprimir imagens e confirmar capa e imagens internas carregando.
4. Executar `python scripts/update_sitemap.py`.
5. Executar `python scripts/update_sitemap.py --check` e validar a contagem `static + news + videos + competitions + events`, XML, URLs únicas e ausência de fragmentos inválidos como `#U` ou `%23U`.
6. Fazer commit apenas dos arquivos relacionados e push para `origin/main`.
7. Confirmar a URL, imagem, layout e sitemap no domínio público.
8. No Google Search Console, entrar somente como `tvduasrodas@gmail.com`, reenviar `https://tvduasrodas.com/sitemap.xml` após o lote publicado e solicitar indexação das URLs novas. Nunca usar `wesleyrodrigo29@gmail.com`.
9. Concluir os passos 1 a 8 imediatamente após o push. Não aguardar a execução das 20h; às 20h apenas auditar e corrigir pendências.

### Recuperação obrigatória de publicação

Para cada lote, seguir esta ordem sem antecipar o uso do plugin Computer Use:

1. Fazer diretamente o commit somente dos arquivos relacionados à tarefa.
2. Se o commit direto funcionar, tentar diretamente o push para `origin/main`.
3. Se não for possível fazer o commit direto, abrir uma nova tarefa com o plugin Computer Use para fazer o commit e o push pelo GitHub Desktop.
4. Se o commit direto funcionar, mas o push remoto direto falhar, abrir uma nova tarefa com o plugin Computer Use para fazer o push manual pelo GitHub Desktop.
5. Na nova tarefa, usar exatamente esta instrução, sem acrescentar ou remover texto: `abrir Github Desktop app e fazer commit de tarefas pendentes em caso nao houver necessidate de fazer commit fazer push.`
6. Usar exclusivamente o clone `C:\Users\Wesley\Documents\TVDUASRODAS\tvduasrodas`; nunca usar o clone antigo em `Documents\GitHub`.
7. Se a nova tarefa concluir a publicação, retomar imediatamente a programação restante, incluindo validação pública, sitemap e Search Console quando aplicável.
8. Se ainda não for possível publicar, enviar e-mail imediato a Wesley com o commit pendente, horário Eastern e erro resumido, para intervenção manual. Continuar tarefas independentes.

## Regras permanentes

- Repositório único: `C:\Users\Wesley\Documents\TVDUASRODAS\tvduasrodas`, branch `main`.
- Nunca alterar ou publicar no projeto `itservices` nem no clone antigo do GitHub Desktop.
- Priorizar fontes oficiais, imagens de imprensa licenciadas e créditos corretos.
- Não deixar publicação válida somente no computador: validar, fazer commit, push e confirmar no site.
- Toda execução gera relatório visível: checado sem novidade, publicado com URL ou ação necessária.
- CAPTCHA, 2FA, novo OAuth, pagamento ou nova permissão exigem Wesley; tarefas independentes continuam.
