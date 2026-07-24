# Rotina diária fixada — TVDUASRODAS

Versão atualizada em 24 de julho de 2026. Esta rotina é obrigatória para o worker e não pode ser reduzida, substituída ou ignorada sem uma nova instrução expressa de Wesley. O portal não é somente competições e eventos.

## Sincronização obrigatória entre este arquivo e as automações

- Este arquivo é a fonte principal e soberana das regras de todas as automações da TVDUASRODAS.
- Todas as regras universais deste arquivo se aplicam a todas as automações atuais e futuras do projeto e a cada ocorrência programada, sem diferença de rigor entre horários.
- Sempre que qualquer configuração, prompt, horário, escopo, formato, ferramenta, recuperação ou regra de uma automação for criada ou alterada, a mesma mudança deve ser registrada neste arquivo durante a mesma execução.
- Uma alteração de automação não pode ser considerada concluída enquanto este arquivo não estiver sincronizado, validado, incluído em commit e publicado em `origin/main`.
- Se existir diferença entre a configuração de uma automação e este arquivo, interromper o encerramento, corrigir a divergência e aplicar a recuperação obrigatória de publicação.
- O relatório da alteração deve confirmar explicitamente: `configuração da automação atualizada`, `ROTINA-DIARIA-AUTOMACAO.md sincronizado`, `commit publicado` e `origin/main confirmado`.

## Isolamento obrigatório de cada janela automatizada

- Cada ocorrência de qualquer automação — horários editoriais às **08h, 11h, 14h, 17h e 20h**, horários do Instagram às **08h30, 11h30, 14h30, 17h30 e 20h30** e auditorias de recuperação às **08h40, 11h40, 14h40, 17h10 e 20h10**, em `America/New_York` — deve iniciar em uma **nova tarefa independente do Codex**. É proibido continuar qualquer execução automática em uma tarefa usada por outra ocorrência, mesmo quando pertencer à mesma automação.
- A primeira ação da nova tarefa deve ser abrir e ler **integralmente** `C:\Users\Wesley\Documents\TVDUASRODAS\tvduasrodas\ROTINA-DIARIA-AUTOMACAO.md`. Nenhuma pesquisa, diagnóstico, seleção de pauta, edição, publicação ou uso da memória pode ocorrer antes dessa leitura.
- Nenhum skill, memória, navegador, pesquisa, diagnóstico, arquivo auxiliar ou outra ferramenta pode ser consultado antes da leitura integral deste documento.
- Depois da leitura, este arquivo deve ser tratado como **autoridade operacional absoluta** para toda a janela. Conversas anteriores, resumos e memória são apenas contexto e nunca podem reduzir, substituir, reinterpretar ou adiar uma regra obrigatória daqui.
- A memória da automação pode ser consultada somente **depois** da leitura integral deste arquivo e serve para continuidade factual e prevenção de duplicidade, não para transportar o peso ou o raciocínio da tarefa anterior.
- Se a execução perceber que não está em uma tarefa nova e independente, deve interromper o trabalho nessa tarefa e iniciar uma nova tarefa antes de prosseguir. Não é permitido compensar essa falha resumindo ou limpando a conversa existente.
- A execução deve declarar no primeiro resumo interno da janela: `nova tarefa confirmada`, `ROTINA-DIARIA-AUTOMACAO.md lida integralmente`, data, dia da semana e horário calculados em Eastern.

## Visibilidade obrigatória da última tarefa automática

- A tarefa criada para cada ocorrência automática nunca deve ser arquivada ao concluir.
- Ao finalizar a execução, depois do relatório e de todas as validações obrigatórias, usar a ferramenta nativa de navegação do Codex para abrir e manter visível a própria tarefa da ocorrência. A última tarefa automática concluída deve permanecer como a tarefa aberta no aplicativo, para que Wesley veja imediatamente onde a automação parou.
- Nunca usar Computer Use para controlar a interface do Codex. Para abrir a tarefa, usar somente a ferramenta nativa de navegação de tarefas do aplicativo.
- Se a navegação para a própria tarefa não estiver disponível, manter a tarefa sem arquivamento, entregar a resposta final completa e registrar no relatório que a abertura automática da tarefa não pôde ser confirmada.
- Não retornar automaticamente a uma tarefa anterior depois da conclusão. A ocorrência mais recente tem prioridade de visibilidade.

## Particionamento das automações e aplicação das regras

Existem quatro configurações ativas vinculadas ao projeto `TVDUASRODAS`, organizadas em três rotinas lógicas:

1. `Atualizações otimizadas TV Duas Rodas`: uma única configuração executada às **08h, 11h, 14h, 17h e 20h**. O horário determina qual janela editorial deste documento deve ser executada; todas as regras universais, especialmente leitura inicial, isolamento, qualidade, validação, commit, push, recuperação, Search Console e relatório, valem igualmente nas cinco ocorrências.
2. `Instagram TVDUASRODAS — Reels e Stories`: uma única configuração executada às **08h30, 11h30, 14h30, 17h30 e 20h30**. Todas as regras universais valem igualmente nas cinco ocorrências, acrescidas das regras específicas da seção **Instagram — somente Reels e Stories**.
3. `Recuperação de pendências TVDUASRODAS`: uma única rotina lógica implementada por duas configurações coordenadas, porque o agendador exige grupos com o mesmo minuto:
   - `Recuperação de pendências TVDUASRODAS — manhã e tarde`, às **08h40, 11h40 e 14h40**.
   - `Recuperação de pendências TVDUASRODAS — fim do dia`, às **17h10 e 20h10**.
   As duas usam as mesmas regras, auditam se as ocorrências editoriais e de Instagram anteriores rodaram e terminaram corretamente, retomam trabalhos pausados ou com falha e concluem todo backlog executável sem duplicar publicações.

- É proibido criar versões de regras diferentes por horário dentro da mesma automação. Uma regra universal adicionada ou alterada deve ser aplicada à configuração completa e, portanto, a todas as ocorrências daquela automação.
- Diferenças entre horários podem existir somente no trabalho editorial específico descrito nas seções 08h, 11h, 14h, 17h e 20h, nunca nas regras de leitura obrigatória, isolamento, autorização, commit, push, recuperação ou confirmação remota.
- Se uma nova automação for criada para este projeto, ela deve ser adicionada a esta seção e receber integralmente o bloco universal de leitura, isolamento, publicação e recuperação antes de ser ativada.

## Auditoria automática e recuperação de pendências

- Em cada horário de recuperação, perguntar operacionalmente: `Existe alguma pendência vencida e executável nas automações editorial ou de Instagram?` A resposta deve vir de uma auditoria real do repositório, das páginas públicas, dos registros de publicação, dos estados de eventos e competições, da matriz de fontes confiáveis e das execuções anteriores; nunca de suposição.
- Conferir se a janela imediatamente anterior foi iniciada, se publicou tudo que era obrigatório e se chegou a commit, push, validação pública, sitemap, Search Console e registro final. Para Instagram, conferir Story e Reel separadamente e nunca exigir Feed.
- Detectar também pendências antigas ainda abertas, incluindo estados `FALHA`, `PENDENTE`, `NAO_ELEGIVEL_URL_INDISPONIVEL` que possam ter mudado, arquivos locais sem commit, branch à frente do remoto, URL já pública sem SEO concluído, evento com situação incompatível com a data e cobertura T+1 vencida.
- Quando houver ação executável, a automação de recuperação assume imediatamente a autorização permanente de Wesley para pesquisar, editar, gerar mídia, publicar no portal, publicar Story e Reel, usar as sessões autenticadas, solicitar indexação, fazer commit e enviar para `origin/main`. Não pedir novamente autorização para essas ações previstas.
- A recuperação deve reexecutar somente a parte faltante e preservar idempotência. Antes de criar ou publicar, consultar URLs, slugs e `output/instagram/publication-log.json` para não repetir matéria, Story ou Reel já confirmado.
- Não considerar como pendência vencida um balanço cuja data futura ainda não chegou nem uma solicitação do Google já aceita e ainda em processamento. A indisponibilidade de uma única fonte não encerra a busca: consultar áreas de resultados, documentos, prestadores contratados e fontes secundárias confiáveis conforme a matriz. Somente a ausência de dados após essa auditoria ampliada pode ser registrada como monitoramento externo, sem inventar informações.
- CAPTCHA, 2FA, novo OAuth, pagamento ou nova permissão continuam exigindo Wesley. Esses bloqueios não autorizam contornar proteções e não impedem a conclusão de tarefas independentes.
- A ocorrência somente pode encerrar depois de concluir todas as pendências executáveis encontradas, validar o resultado, publicar os arquivos relacionados e confirmar `HEAD == origin/main`. Se nada estiver vencido, registrar objetivamente `nenhuma pendência executável`.

## Metas editoriais mínimas do dia

Antes de escolher ou classificar qualquer pauta, calcular novamente a data e o dia da semana em `America/New_York`. Não reutilizar o dia da semana registrado por uma execução anterior. Declarar no resumo da janela o dia calculado e o programa correspondente. Se uma urgência editorial substituir a grade fixa, registrar explicitamente a exceção e o motivo.

Até o encerramento das 20h (horário Eastern), o worker deve entregar:

1. Pelo menos **uma matéria nova e independente para a Revista**, com `contentType: "article"`. Matéria própria, notícia e edição de programa são tipos diferentes; notícia e programa não substituem esta meta.
2. Nos dias da grade fixa, **uma nova edição do programa correspondente**, com `contentType: "program"`, além da matéria diária. A edição deve ser identificada como a edição daquela semana e nunca pode ser contada como matéria diária.
3. Pelo menos **um vídeo novo para a TV com áudio em português brasileiro**, incorporado do YouTube, confiável, não duplicado e classificado na categoria correta. Vídeo em inglês, espanhol ou outro idioma não cumpre a meta, mesmo quando título e descrição estiverem traduzidos.
4. Diversificar a TV durante a semana: não repetir categoria de vídeo nem canal de origem na mesma semana editorial, salvo transmissão ou atualização oficial urgente, com exceção explicada no relatório. Alternar testes, competições, cross, eventos, urbano, lançamentos, dicas, tecnologia, viagem, história, customização, entretenimento e outras categorias pertinentes.
5. Todas as **atualizações urgentes de competições e eventos** encontradas na matriz obrigatória de fontes confiáveis: resultados, classificação, liderança, calendário ou informação de serviço.
6. **SEO, sitemap, publicação, validação pública e Google Search Console imediatamente após cada lote publicado**, sem esperar o fechamento das 20h.

### Rotação semanal de matérias

- Toda matéria própria deve usar `contentType: "article"` e uma categoria ainda não usada por outra matéria própria na mesma semana, de segunda a domingo.
- Se uma matéria própria da categoria Cross já foi publicada naquela semana, a próxima matéria própria deve usar outra categoria.
- Notícias factuais usam `contentType: "news"` e podem repetir categoria quando houver novidade real, desdobramento ou atualização verificável.
- Edições de programa usam `contentType: "program"` e não participam da contagem da matéria diária nem da rotação de categorias das matérias próprias.
- Notícia cujo conteúdo principal seja agenda, serviço ou programação deve ir para Eventos. Resultado, classificação, etapa, liderança ou calendário esportivo deve atualizar Competições. Só publicar também na Revista quando existir uma reportagem editorial própria, com contexto e valor além da atualização estrutural.

## Regra obrigatória de anúncios contextuais

- Todo anúncio exibido em matéria, artigo, programa, vídeo, competição ou evento deve corresponder ao tema principal do conteúdo. É proibido exibir campanha de Bicicletas em conteúdo de Motos, campanha de Motos em conteúdo de Scooters ou qualquer outra combinação incompatível.
- As categorias publicitárias oficiais são: `motos`, `bicicletas`, `scooters`, `eletricos`, `mobilidade`, `tecnologia`, `competicoes`, `eventos` e `geral`.
- Toda nova publicação deve receber `ad_category` explícita quando houver ambiguidade. Quando o campo estiver vazio, o sistema pode inferir a categoria por título, categoria editorial, programa, modalidade, tipo de evento, tags e texto. A automação deve revisar a inferência antes de publicar; `geral` é apenas fallback e não deve substituir uma categoria identificável.
- Campanhas e patrocinadores são administrados centralmente em `content/ads/config.json`. É proibido gravar o patrocinador diretamente em uma única matéria ou trocar banners página por página. A inclusão ou substituição de uma campanha de Scooters, por exemplo, deve atualizar automaticamente todos os espaços elegíveis de conteúdos classificados como Scooters.
- Os formatos comerciais oficiais são:
  1. `retangulo-lateral-300` — **Retângulo Lateral 300**, criação de 300 × 250 px, no topo da lateral de matérias e vídeos.
  2. `faixa-editorial-728` — **Faixa Editorial 728**, criação de 728 × 90 px, no meio da matéria e na área contextual do vídeo.
  3. `billboard-cobertura-970` — **Billboard de Cobertura 970**, criação de 970 × 250 px, em competições, eventos e páginas especiais.
- Em matéria ou programa individual são obrigatórios dois espaços: o Retângulo Lateral 300 antes de `Mais matérias` e a Faixa Editorial 728 inserida no meio real do corpo editorial. A faixa nunca deve ficar imediatamente abaixo da imagem hero.
- Em vídeo, o Retângulo Lateral 300 e a Faixa Editorial 728 devem acompanhar a categoria do vídeo selecionado no player e mudar quando o usuário selecionar outro vídeo.
- Em competição ou evento, o Billboard de Cobertura 970 deve usar primeiro a modalidade ou o tema específico: MTB, BMX e ciclismo recebem Bicicletas; MotoGP, motocross, enduro e similares recebem Motos; festivais ou feiras sem produto predominante podem receber Eventos.
- Campanha com situação inativa, data futura ou período encerrado não pode aparecer. Na ausência de campanha ativa da categoria e do formato, usar somente a campanha institucional `geral`.
- No celular, as peças devem ser responsivas, preservar proporção, legibilidade, área segura e link. A dimensão comercial continua sendo a criação desktop registrada no plano.
- Antes de encerrar qualquer alteração publicitária, validar pelo menos uma página de Motos e uma de Bicicletas, confirmar categorias diferentes no DOM, conferir os dois espaços da matéria, testar troca de vídeo, competição/evento, responsividade, links e ausência de deslocamento de layout.
- Nomes, dimensões, regras de venda, pacotes e requisitos ficam documentados em `PLANO-COMERCIAL-ANUNCIOS.md`. Mudanças de formato exigem atualização simultânea desse plano, desta rotina, de `content/ads/config.json` e das automações.

## Matriz obrigatória de fontes confiáveis para eventos e competições

É proibido concluir que “não há resultado”, “não há classificação” ou “a fonte oficial ainda não publicou” depois de consultar somente a página principal, a área de notícias ou um único domínio. Para cada campeonato, torneio, etapa, rodada ou evento, a pesquisa deve percorrer a matriz abaixo e procurar também páginas, PDFs, planilhas, APIs, arquivos para download e plataformas externas vinculadas.

1. **Fonte primária reguladora:** federação, confederação, liga, entidade sancionadora ou organizador responsável.
2. **Área específica de dados:** páginas de resultados, ranking, classificação, documentos oficiais, comunicados, calendário, regulamento e arquivos anexos da entidade. A área de notícias nunca substitui essa verificação.
3. **Prestador oficial contratado:** empresa de cronometragem, inscrição, apuração, live timing, arbitragem ou gestão esportiva indicada pelo organizador, como plataformas externas de resultados. Quando estiver vinculada pela entidade ou pelo regulamento, essa plataforma é uma fonte primária autorizada mesmo estando em outro domínio.
4. **Fontes primárias complementares:** federação estadual ou nacional parceira, equipe, piloto/atleta, fabricante, circuito, promotor local ou assessoria oficial, usadas para confirmar fatos específicos e localizar documentos.
5. **Fontes secundárias confiáveis:** veículos especializados estabelecidos, agências de notícias e imprensa regional com autoria, data, identificação do evento e dados verificáveis. Servem para descoberta, contexto e confirmação cruzada; rumor, perfil anônimo, agregador sem origem e reprodução sem autoria não servem.

- Usar **uma ou mais fontes confiáveis**, nunca limitar a pesquisa artificialmente a um único site. Sempre que disponível, pelo menos uma fonte deve ser primária ou um prestador oficialmente contratado.
- Para resultado, pódio, pontos ou classificação, buscar confirmação em **duas fontes confiáveis** quando houver risco de atualização, divergência ou documento provisório. Se existir apenas um documento primário completo e inequívoco, ele pode sustentar a atualização, mas a busca nas demais camadas deve ser registrada.
- Se somente fontes secundárias confiáveis tiverem publicado o dado, exigir pelo menos duas confirmações independentes, identificar a informação como provisória quando couber e substituir pela tabela primária assim que ela aparecer.
- Não publicar apenas o vencedor quando houver tabela completa. Atualizar `standings`, `latest_result`, `rounds`, vencedor, pontos, liderança, `results_url`, data da checagem e links dos documentos disponíveis.
- Em divergência, preservar o dado anterior, registrar as versões conflitantes e procurar regulamento, júri, boletim ou documento posterior. A fonte mais recente e com autoridade direta prevalece.
- Antes de declarar ausência de dados, registrar no controle editorial quais camadas foram consultadas, URLs, data e horário. “Sem publicação” só é um estado válido depois dessa busca ampliada.

## Descoberta obrigatória de eventos ainda não cadastrados

- A cobertura não pode se limitar aos itens já presentes no portal. Nas janelas de 08h e 17h e nas auditorias de recuperação, pesquisar calendários nacionais e internacionais de motociclismo, ciclismo, MTB, BMX, estrada, pista, paraciclismo, motocross, supercross, arena cross, enduro, hard enduro, rally, rally raid, baja, trial, motovelocidade, scooter, e-bike, mobilidade, encontros, festivais, feiras, salões e demais modalidades relacionadas às duas rodas.
- Cruzar calendários de confederações, federações, ligas, organizadores, circuitos, plataformas oficiais contratadas e veículos especializados confiáveis. Verificar Brasil, América Latina e competições internacionais relevantes ao público brasileiro.
- Ao localizar evento confirmado ainda não cadastrado, criar ou atualizar imediatamente a página estrutural, calendário, datas, modalidade, local, fonte e situação. Não esperar o evento começar para cadastrá-lo.
- Eventos e competições descobertos depois da abertura entram imediatamente no fluxo de recuperação: cadastrar, corrigir situação, incorporar resultados/classificação já disponíveis e cumprir as coberturas de abertura e encerramento sem duplicação.

## Cobertura obrigatória de abertura, encerramento e situação

Esta regra vale para **todos os eventos e todas as competições** cadastrados, nacionais ou internacionais, inclusive festivais, feiras, encontros, campeonatos, etapas e rodadas de vários dias.

1. Em toda ocorrência editorial, comparar a data atual em `America/New_York` com `start_date` e `end_date`, conferir o canal oficial e atualizar a situação estrutural:
   - Eventos: `proximo` antes da abertura, `em_andamento` entre início e fim, `encerrado` depois do último dia e `cancelado` somente com confirmação oficial.
   - Competições/campeonatos: `agendada` antes do início, `em_andamento` durante a temporada ou etapa, `concluida` depois do encerramento e `cancelado` somente com confirmação oficial. Aplicar o mesmo controle a cada item de `rounds`.
   - Adiamento, mudança de data ou interrupção devem atualizar imediatamente datas, resumo, calendário e fonte oficial; nunca tratar ausência de notícia como cancelamento.
2. No **dia seguinte ao primeiro dia** de cada evento ou competição, publicar obrigatoriamente uma notícia original na Revista explicando como foi a abertura. A matéria deve usar fonte oficial publicada depois da abertura, registrar fatos confirmados, destaques, serviço para os dias restantes e linkar a página estrutural do evento ou campeonato.
3. No **dia seguinte ao último dia**, publicar obrigatoriamente uma matéria de balanço completo: principais acontecimentos, resultados ou atrações, vencedores e classificação quando houver, números oficiais disponíveis, contexto e próximos passos. Atualizar a página estrutural para `encerrado` ou `concluida` no mesmo lote.
4. Em competição ou evento de **um único dia**, a matéria publicada no dia seguinte deve ser um balanço completo único e cumprir simultaneamente as obrigações de abertura e encerramento; não criar dois textos artificiais sobre o mesmo fato.
5. Em competições por etapas, a obrigação se aplica à etapa/rodada monitorada: primeiro dia no dia seguinte à abertura da etapa e balanço no dia seguinte ao seu término. A página da temporada permanece `em_andamento` enquanto houver etapa futura confirmada.
6. Não declarar presença da TVDUASRODAS, público, resultado, ocorrência, show realizado ou experiência presencial sem confirmação. Quando a primeira fonte consultada ainda não tiver publicado o balanço necessário, percorrer toda a matriz de fontes confiáveis. Só depois dessa busca ampliada registrar a obrigação como monitoramento externo; refazer a busca nas janelas seguintes e publicar assim que houver confirmação suficiente.
7. Antes de criar a matéria, verificar duplicidade por evento, competição, etapa, data e tipo de balanço. Registrar a cobertura na página estrutural ou no controle editorial para impedir publicação duplicada.
8. Cada notícia de abertura ou encerramento é conteúdo novo elegível para um Story e um Reel na próxima ocorrência da automação do Instagram, seguindo a regra de apenas uma publicação por formato e sem Feed.

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
- Auditar situações e obrigações T+1 de todos os eventos, competições e rodadas. Publicar antes das pautas discricionárias qualquer matéria de primeiro dia ou balanço final vencida, além de corrigir `proximo/agendada`, `em_andamento`, `encerrado/concluida` ou `cancelado` conforme fonte oficial.
- Fazer a **primeira verificação obrigatória de SEO do dia** com `python scripts/update_sitemap.py --check`.
- Conferir se o fechamento de SEO do dia anterior foi concluído: sitemap gerado depois da última publicação, enviado ao Google Search Console e URLs novas solicitadas para indexação. Se faltar qualquer etapa, corrigir, publicar e concluir usando somente `tvduasrodas@gmail.com` antes de seguir.
- Se o sitemap estiver desatualizado, executar `python scripts/update_sitemap.py`, validar a contagem por coleção, publicar e reenviar o sitemap no Search Console.
- Verificar de forma incremental salas de imprensa brasileiras, fabricantes, Abraciclo, recalls, CBM, CBC, áreas específicas de resultados/ranking, prestadores oficiais contratados e calendários já monitorados.
- Fazer descoberta ativa de eventos e competições ainda não cadastrados, seguindo a matriz de fontes; não limitar a auditoria ao acervo existente.
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

- Verificar resultados, pódios, pontos, liderança, etapas e calendários em todas as camadas da matriz de fontes confiáveis, incluindo PDFs, planilhas, APIs e prestadores oficiais em domínios externos.
- Repetir a auditoria de situação e de matérias T+1. Se a primeira fonte de uma abertura ou encerramento ainda não estava disponível às 08h, pesquisar novamente em toda a matriz e publicar o balanço assim que houver confirmação suficiente.
- Atualizar páginas existentes e preservar histórico; não publicar apenas o vencedor quando a tabela oficial completa estiver disponível.
- Verificar eventos nacionais e internacionais relevantes ao público brasileiro e cadastrar os confirmados que ainda não existam no portal.
- Se não houver mudança esportiva, procurar notícia relevante de produto, mercado, recall, segurança, mobilidade ou ciclismo. A janela não termina apenas com “sem novidade em competições”.

## 20h — Fechamento obrigatório e auditoria final de SEO

- Rodar `python scripts/check_daily_targets.py --require-complete`.
- Confirmar que nenhuma obrigação vencida de matéria do primeiro dia ou do balanço final ficou sem publicação e que todas as situações de eventos, campeonatos e rodadas refletem datas e comunicados oficiais.
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

1. Executar Git sempre dentro de `C:\Users\Wesley\Documents\TVDUASRODAS\tvduasrodas`. Antes de declarar que Git está indisponível, localizar o executável com `load_workspace_dependencies`. Nesta instalação, usar `C:\Users\Wesley\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe`. Para operações HTTPS, definir `GIT_EXEC_PATH` como `C:\Users\Wesley\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\mingw64\bin` e acrescentar ao `PATH` as pastas `mingw64\bin`, `usr\bin` e `cmd` dessa instalação. A ausência do comando curto `git` no `PATH` não é falha de publicação.
2. Fazer diretamente o commit somente dos arquivos relacionados à tarefa.
3. Se o commit direto funcionar, tentar diretamente o push para `origin/main`. Se a rede estiver bloqueada pelo ambiente protegido, solicitar a liberação de rede prevista pela ferramenta e repetir o push; isso não deve ser tratado como pedido manual de autorização a Wesley.
4. Se não for possível fazer o commit direto, ou se o push remoto direto falhar mesmo após configurar o Git empacotado e liberar a rede, usar o plugin Computer Use **diretamente na mesma tarefa da automação** para controlar o GitHub Desktop. É proibido chamar `list_projects`, `create_thread`, abrir uma segunda tarefa ou depender do serviço de tarefas para essa recuperação.
5. Inicializar o Computer Use pelo `SKILL.md` do plugin e pelo `node_repl`; ler obrigatoriamente a documentação `guidance` e `confirmations`, listar os aplicativos, selecionar exatamente uma janela do GitHub Desktop e confirmar visualmente o repositório `tvduasrodas` e a branch `main`.
6. No GitHub Desktop, fazer commit somente dos arquivos relacionados ao lote quando houver alterações; se o commit já existir, clicar diretamente em `Push origin`. A automação contém autorização inicial, explícita e permanente de Wesley para enviar somente os arquivos desse lote ao repositório `tvduasrodas/tvduasrodas`, branch `main`, no GitHub. Não pedir confirmação adicional para `Commit` ou `Push origin`.
7. Usar exclusivamente o clone `C:\Users\Wesley\Documents\TVDUASRODAS\tvduasrodas`; nunca usar o clone antigo em `Documents\GitHub`.
8. Depois do clique, aguardar a conclusão e atualizar o estado da janela. Só considerar o fallback manual concluído quando o GitHub Desktop exibir `push complete`, `Fetch origin` sem commits pendentes ou estado equivalente, e zero arquivos alterados.
9. Se `list_apps`, `list_windows` ou outra chamada leve do Computer Use expirar, aguardar dois segundos e repetir uma vez. Se expirar novamente, reiniciar a sessão JavaScript, reinicializar o Computer Use e tentar mais uma vez, conforme a recuperação oficial do skill. Não substituir esse procedimento por `list_projects`.
10. Se uma janela, captura ou ativação falhar, refazer a seleção do GitHub Desktop e tentar uma vez com o objeto de janela atualizado. Nunca reutilizar coordenadas, índices ou capturas antigas.
11. Depois do fallback pelo GitHub Desktop, executar `git status --porcelain=v1 --branch`, comparar `git rev-parse HEAD` com `git ls-remote origin refs/heads/main` e somente confirmar sucesso quando os SHAs forem idênticos e não houver arquivos relevantes fora de commit.
12. Se ainda não for possível publicar depois da tentativa direta pelo Git empacotado, liberação de rede e recuperação direta pelo Computer Use, enviar e-mail imediato a Wesley com o commit pendente, horário Eastern e os erros exatos de cada tentativa. Continuar tarefas independentes.

## Regras permanentes

- Repositório único: `C:\Users\Wesley\Documents\TVDUASRODAS\tvduasrodas`, branch `main`.
- Nunca alterar ou publicar no projeto `itservices` nem no clone antigo do GitHub Desktop.
- Priorizar fontes oficiais, imagens de imprensa licenciadas e créditos corretos.
- Não deixar publicação válida somente no computador: validar, fazer commit, push e confirmar no site.
- A autorização permanente cobre commit, clique em `Push origin`, push para `origin/main` e confirmação remota de todos os lotes previstos por esta rotina. Não pedir nova autorização para essas ações.
- Toda execução gera relatório visível: checado sem novidade, publicado com URL ou ação necessária.
- CAPTCHA, 2FA, novo OAuth, pagamento ou nova permissão exigem Wesley; tarefas independentes continuam.
