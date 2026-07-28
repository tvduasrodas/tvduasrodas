# Rotina diária fixada — TVDUASRODAS

Versão atualizada em 28 de julho de 2026. Esta rotina é obrigatória para o worker e não pode ser reduzida, substituída ou ignorada sem uma nova instrução expressa de Wesley. O portal não é somente competições e eventos.

## Sincronização obrigatória entre este arquivo e as automações

- Este arquivo é a fonte principal e soberana das regras de todas as automações da TVDUASRODAS.
- Todas as regras universais deste arquivo se aplicam a todas as automações atuais e futuras do projeto e a cada ocorrência programada, sem diferença de rigor entre horários.
- Sempre que qualquer configuração, prompt, horário, escopo, formato, ferramenta, recuperação ou regra de uma automação for criada ou alterada, a mesma mudança deve ser registrada neste arquivo durante a mesma execução.
- Uma alteração de automação não pode ser considerada concluída enquanto este arquivo não estiver sincronizado, validado, incluído em commit e publicado em `origin/main`.
- Se existir diferença entre a configuração de uma automação e este arquivo, interromper o encerramento, corrigir a divergência e aplicar a recuperação obrigatória de publicação.
- O relatório da alteração deve confirmar explicitamente: `configuração da automação atualizada`, `ROTINA-DIARIA-AUTOMACAO.md sincronizado`, `commit publicado` e `origin/main confirmado`.

## Autorização inicial, permanente e integral das automações programadas

- Wesley concede antecipadamente às quatro automações ativas e a todas as suas ocorrências programadas **100% de autorização operacional dentro do escopo desta rotina**. Essa autorização já existe antes de cada execução e não precisa ser solicitada, renovada ou confirmada no início, durante ou no fim da ocorrência.
- A autorização cobre pesquisar e selecionar pautas; criar, editar, corrigir e publicar páginas; atualizar eventos, competições, calendários, resultados e classificações; produzir e publicar Story e Reel na conta profissional `@tvduasrodasofc`; gerar, otimizar e excluir arquivos temporários conforme a retenção; atualizar SEO, sitemap e Search Console; usar sessões autenticadas já disponíveis; validar o domínio público; criar commits; enviar os arquivos relacionados para `tvduasrodas/tvduasrodas`, branch `main`; e confirmar `HEAD == origin/main`.
- Quando uma publicação ou atualização estiver prevista pelas regras e passar nas verificações factuais, editoriais, técnicas, de direitos e de não duplicidade, a automação deve executá-la imediatamente. É proibido pausar, deixar como rascunho, adiar para outra janela ou pedir a Wesley frases como “posso publicar?”, “autoriza o push?”, “aprova esta publicação?” ou confirmação equivalente.
- Diálogos de liberação de rede, escrita, navegador, Git ou outra capacidade apresentados pela infraestrutura são etapas técnicas de execução, não pedidos de nova autorização editorial. A automação deve acionar a liberação prevista pela própria ferramenta e continuar automaticamente, sem converter essa etapa em uma pergunta manual a Wesley.
- A autorização permanente não elimina controles de qualidade, segurança, direitos autorais, idempotência, validação ou escopo. Ela vale somente para as ações previstas nesta rotina, no portal TVDUASRODAS, na conta `@tvduasrodasofc`, no Search Console autorizado e no repositório `tvduasrodas/tvduasrodas`, branch `main`; não autoriza outros projetos, contas, repositórios, destinatários ou ações alheias ao lote.
- Somente um bloqueio externo que não possa ser concluído com as credenciais, sessões e permissões já concedidas — CAPTCHA, 2FA, novo OAuth, pagamento ou nova permissão de terceiro — pode exigir Wesley. Mesmo nesses casos, pausar apenas a etapa bloqueada, registrar exatamente o impedimento e continuar todas as tarefas independentes autorizadas.
- Uma ocorrência com trabalho publicável não pode terminar apenas com plano, arquivos locais, prévia, rascunho, commit não enviado ou pedido de aprovação. O estado final obrigatório é publicação confirmada, validação concluída, commit publicado e `origin/main` confirmado, salvo bloqueio externo real documentado.

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

Existem cinco configurações ativas vinculadas ao projeto `TVDUASRODAS`, organizadas em quatro rotinas lógicas:

1. `Atualizações otimizadas TV Duas Rodas`: uma única configuração executada às **08h, 11h, 14h, 17h e 20h**. O horário determina qual janela editorial deste documento deve ser executada; todas as regras universais, especialmente leitura inicial, isolamento, qualidade, validação, commit, push, recuperação, Search Console e relatório, valem igualmente nas cinco ocorrências.
2. `Instagram TVDUASRODAS — Reels e Stories`: uma única configuração executada às **08h30, 11h30, 14h30, 17h30 e 20h30**. Todas as regras universais valem igualmente nas cinco ocorrências, acrescidas das regras específicas da seção **Instagram — somente Reels e Stories**.
3. `Radar de datas editoriais TVDUASRODAS`: uma configuração executada às **07h15 e 15h15**. Ela antecipa a descoberta de datas brasileiras, efemérides, campanhas, aniversários, marcos esportivos e oportunidades sazonais, publica no portal toda pauta imediata confirmada e encaminha candidatos sociais para a seleção limitada do Instagram. O radar não publica diretamente no Instagram e não substitui a varredura geral das cinco janelas editoriais.
4. `Recuperação de pendências TVDUASRODAS`: uma única rotina lógica implementada por duas configurações coordenadas, porque o agendador exige grupos com o mesmo minuto:
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
- Auditar a fila editorial geral, inclusive notícias, lançamentos, recalls, efemérides, eventos e resultados descobertos e ainda não concluídos. Toda pauta `publicavel` vencida é pendência executável, mesmo quando as metas mínimas do dia já tiverem sido cumpridas.
- Para o Instagram, conferir a fila e o total de pautas do dia antes de recuperar. Concluir formatos faltantes de uma pauta já contabilizada, mas nunca publicar uma sexta pauta ou mais de uma pauta nova na mesma janela.
- Quando houver ação executável, a automação de recuperação assume imediatamente a autorização permanente de Wesley para pesquisar, editar, gerar mídia, publicar no portal, publicar Story e Reel, usar as sessões autenticadas, solicitar indexação, fazer commit e enviar para `origin/main`. Não pedir novamente autorização para essas ações previstas.
- A recuperação deve reexecutar somente a parte faltante e preservar idempotência. Antes de criar ou publicar, consultar URLs, slugs e `output/instagram/publication-log.json` para não repetir matéria, Story ou Reel já confirmado.
- Não considerar como pendência vencida um balanço cuja data futura ainda não chegou nem uma solicitação do Google já aceita e ainda em processamento. A indisponibilidade de uma única fonte não encerra a busca: consultar áreas de resultados, documentos, prestadores contratados e fontes secundárias confiáveis conforme a matriz. Somente a ausência de dados após essa auditoria ampliada pode ser registrada como monitoramento externo, sem inventar informações.
- CAPTCHA, 2FA, novo OAuth, pagamento ou nova permissão continuam exigindo Wesley. Esses bloqueios não autorizam contornar proteções e não impedem a conclusão de tarefas independentes.
- A ocorrência somente pode encerrar depois de concluir todas as pendências executáveis encontradas, validar o resultado, publicar os arquivos relacionados e confirmar `HEAD == origin/main`. Se nada estiver vencido, registrar objetivamente `nenhuma pendência executável`.

## Classificação dinâmica de relevância de eventos e competições

Esta classificação é exclusivamente interna. O portal nunca deve publicar a pontuação, o nível de confiança, os critérios, os pesos, a tendência ou expressões como “evento pequeno”. Para o público, cada página continua recebendo tratamento informativo respeitoso e serviço completo.

### Duas obrigações independentes

1. **Atualização estrutural universal:** todos os eventos, competições, campeonatos, etapas, rodadas, festivais, torneios, copas, encontros e espetáculos cadastrados, sem exceção, devem ser auditados diariamente. A página deve refletir data e hora locais, fuso horário do local, situação correta e horário da última checagem.
2. **Cobertura editorial T+1 seletiva:** a matéria no dia seguinte ao primeiro dia e o balanço no dia seguinte ao último dia são obrigatórios somente para itens classificados internamente como `alta_relevancia`. Itens `monitoramento` ou `cobertura_estrutural` continuam com página, calendário, serviço, resultados e situação atualizados, mas não geram matéria T+1 automática. Uma novidade jornalística forte ainda pode justificar matéria por decisão editorial, sem transformar a exceção em obrigação permanente.

### Campos internos obrigatórios

Sempre que o formato da coleção permitir, manter estes campos no registro do evento ou competição:

- `timezone`: fuso IANA do local, por exemplo `America/Sao_Paulo`.
- `local_start` e `local_end`: data e hora locais confirmadas; quando o organizador ainda não divulgar o horário, usar valor vazio e registrar a pendência, nunca inventar `00:00`.
- `status`: `agendada`, `em_andamento`, `concluida`, `adiada` ou `cancelada`, conforme datas locais e confirmação oficial.
- `status_checked_at`: data e hora da checagem diária em ISO 8601.
- `relevance_tier`: `alta_relevancia`, `monitoramento` ou `cobertura_estrutural`.
- `relevance_score`: inteiro de 0 a 100.
- `relevance_confidence`: `alta`, `media` ou `baixa`.
- `relevance_evaluated_at`, `relevance_previous_score`, `relevance_trend` e `relevance_reason_codes`.
- `coverage_t1_required`: verdadeiro somente quando `relevance_tier` for `alta_relevancia`.
- `relevance_evidence`: fontes e sinais usados, com data de consulta; este bloco é interno e não deve aparecer na página pública.

Registros antigos sem esses campos não ficam dispensados. A automação deve preenchê-los progressivamente, priorizando itens em andamento, iniciando nos próximos 30 dias ou com sinais recentes de crescimento. A ausência temporária de público ou repercussão verificável reduz a confiança, não autoriza inventar zero.

### Índice de Relevância TVDUASRODAS — IRT

Calcular uma nota de 0 a 100 com evidências comparáveis:

1. **Público e escala presencial — 0 a 25:** média confirmada das últimas edições, capacidade efetivamente usada, participantes/inscritos e visitantes. Considerar o tamanho relativo à cidade: um festival que mobiliza uma pequena cidade pode obter nota máxima mesmo sem público de metrópole.
2. **Repercussão editorial e procura — 0 a 20:** volume e diversidade de publicações recentes, veículos independentes, buscas, vídeos, redes oficiais e crescimento da atenção. Desduplicar republicações do mesmo release e não confundir quantidade artificial com relevância.
3. **Organização e reconhecimento institucional — 0 a 15:** confederação, federação, liga reconhecida, promotora nacional ou internacional, poder público, circuito consolidado e entidades sancionadoras. O nome da entidade é sinal, não decisão automática.
4. **Alcance territorial e atração de público — 0 a 15:** presença de participantes, equipes, expositores ou visitantes de vários estados ou países; transmissão e distribuição nacional; capacidade de atrair deslocamentos.
5. **Tradição, marca e impacto local — 0 a 15:** número e regularidade de edições, reconhecimento espontâneo, ocupação hoteleira, turismo, comércio, trânsito, serviços públicos e importância cultural. Festivais, copas e espetáculos que mobilizam intensamente uma cidade podem ser de alta relevância independentemente do porte do município.
6. **Peso esportivo ou setorial — 0 a 10:** título nacional ou mundial, nível dos atletas/equipes, pontos de campeonato, seletiva oficial, lançamentos, negócios, inovação ou importância para o segmento.

Não usar somente o nome “nacional”, “brasileiro”, “festival”, “copa” ou “campeonato” como prova. Exigir sinais verificáveis e registrar os códigos de razão predominantes.

### Decisão, confiança e estabilidade

- Classificar como `alta_relevancia` quando `relevance_score >= 65` e a confiança for `alta` ou `media`.
- Classificar como `monitoramento` entre 45 e 64, ou quando a nota superar 65 com confiança baixa e ainda exigir confirmação.
- Classificar como `cobertura_estrutural` abaixo de 45, preservando integralmente a atualização diária da página.
- Promoção é imediata quando a nota chegar a 65 com evidência suficiente. Também pode ocorrer por gatilho excepcional confirmado: explosão de interesse, anúncio de atração/atleta de grande projeção, chancela relevante, transmissão nacional, crescimento forte de inscrições, impacto urbano extraordinário ou ampla cobertura independente.
- Para evitar oscilação, rebaixar um item que já era `alta_relevancia` somente quando ficar abaixo de 55 em duas avaliações completas separadas por pelo menos sete dias, salvo cancelamento, fraude de informação ou perda objetiva de escopo.
- Campeonatos e eventos recorrentes são reavaliados por edição e por etapa. A classificação do ano anterior é apenas ponto de partida, nunca herança automática.
- Se fontes confiáveis divergirem, manter a classificação anterior, reduzir `relevance_confidence` e registrar a divergência até nova confirmação.

### Reavaliação e projeção diária

Em todas as janelas editoriais, executar uma varredura leve de sinais para todos os registros; às 08h e às 17h, aprofundar os itens em andamento, nos próximos 30 dias, em `monitoramento` ou com alerta de crescimento. Comparar janelas móveis de 7 e 30 dias com a média histórica e observar:

- aceleração de publicações independentes e buscas;
- ritmo de inscrições, ingressos, credenciais, equipes e expositores;
- novos organizadores, chancelas, transmissões, patrocinadores e atrações;
- ampliação de arena, cidades, etapas, categorias ou duração;
- impacto previsto ou já observado em hotelaria, trânsito, comércio e serviços;
- crescimento de público entre edições e mudança do alcance geográfico.

Definir `relevance_trend` como `subindo`, `estavel` ou `caindo`. Um aumento forte em pelo menos dois grupos independentes de sinais deve abrir alerta de reclassificação, mesmo que o evento fosse pequeno no ciclo anterior. Produzir projeção interna conservadora para a edição atual/próxima, sempre separando dado observado de estimativa. Projeção nunca substitui confirmação factual na página pública.

### Regra operacional para T+1

- Somente `coverage_t1_required: true` entra automaticamente na fila de matéria do primeiro dia e balanço final.
- Evento de alta relevância com um único dia recebe um único balanço T+1 completo.
- Etapas de competição são avaliadas individualmente; a competição pode ser de alta relevância e uma etapa exigir pontuação e evidências próprias.
- Ao promover um item durante ou logo após sua realização, recuperar a cobertura T+1 ainda editorialmente válida. Se o prazo já tiver perdido atualidade, produzir balanço contextual apenas quando houver valor jornalístico real.
- Mudança de data, hora, local, situação ou resultado estrutural nunca depende da classificação: deve ser atualizada para todos.

## Metas editoriais mínimas do dia

Antes de escolher ou classificar qualquer pauta, calcular novamente a data e o dia da semana em `America/New_York`. Não reutilizar o dia da semana registrado por uma execução anterior. Declarar no resumo da janela o dia calculado e o programa correspondente. Se uma urgência editorial substituir a grade fixa, registrar explicitamente a exceção e o motivo.

As metas abaixo são **pisos de produção, nunca tetos**. Não existe limite numérico diário ou por janela para matérias, notícias, eventos, competições, resultados, calendários, lançamentos, recalls, páginas novas, correções ou atualizações do portal. Encontrar uma publicação que cumpra a meta mínima não encerra a pesquisa e não autoriza ignorar outras pautas confirmadas.

Até o encerramento das 20h (horário Eastern), o worker deve entregar:

1. Pelo menos **uma matéria nova e independente para a Revista**, com `contentType: "article"`. Matéria própria, notícia e edição de programa são tipos diferentes; notícia e programa não substituem esta meta.
2. Nos dias da grade fixa, **uma nova edição do programa correspondente**, com `contentType: "program"`, além da matéria diária. A edição deve ser identificada como a edição daquela semana e nunca pode ser contada como matéria diária.
3. Pelo menos **um vídeo novo para a TV com áudio em português brasileiro**, incorporado do YouTube, confiável, não duplicado e classificado na categoria correta. Vídeo em inglês, espanhol ou outro idioma não cumpre a meta, mesmo quando título e descrição estiverem traduzidos.
4. Diversificar a TV durante a semana: não repetir categoria de vídeo nem canal de origem na mesma semana editorial, salvo transmissão ou atualização oficial urgente, com exceção explicada no relatório. Alternar testes, competições, cross, eventos, urbano, lançamentos, dicas, tecnologia, viagem, história, customização, entretenimento e outras categorias pertinentes.
5. Todas as **atualizações estruturais de competições e eventos** encontradas na matriz obrigatória de fontes confiáveis, sem exceção de porte: data e hora locais, fuso, situação, resultados, classificação, liderança, calendário ou informação de serviço. Matérias T+1 obedecem à classificação dinâmica de relevância.
6. **SEO, sitemap, publicação, validação pública e Google Search Console imediatamente após cada lote publicado**, sem esperar o fechamento das 20h.

## Redação permanente, descoberta geral e publicação sem teto

- Em todas as janelas editoriais, o worker funciona como uma redação permanente: descobrir, confirmar, priorizar, criar, atualizar e publicar tudo que for relevante ao universo de duas rodas. É proibido limitar artificialmente a produção a uma matéria, um evento, uma competição, um lançamento ou uma atualização por janela ou por dia.
- Às 08h e 17h, executar uma varredura geral completa. Às 11h, 14h e 20h, atualizar novamente fontes urgentes e publicar qualquer novidade confirmada surgida desde a varredura anterior, além de cumprir o trabalho específico do horário.
- A busca geral deve cobrir, sem se restringir a: motocicletas, scooters, ciclomotores, bicicletas, e-bikes, BMX, MTB, estrada, paraciclismo, mobilidade urbana, elétricos, componentes, acessórios, equipamentos, segurança viária, recalls, legislação, indústria, vendas, produção, tecnologia, lançamentos, testes oficiais, viagens, serviços, encontros, motoclubes, festivais, feiras, salões, calendários, competições, etapas, resultados, classificações, pilotos, equipes e oportunidades editoriais sazonais.
- Pesquisar também notícias recentes de acidentes envolvendo motocicletas, scooters, ciclomotores, bicicletas, e-bikes, triciclos, quadriciclos e demais veículos relacionados ao portal. Priorizar ocorrências com aprendizado público verificável, mudança de trânsito, falha de infraestrutura, defeito, recall, decisão oficial, impacto coletivo ou orientação útil; não explorar tragédia apenas por audiência.
- Percorrer fontes brasileiras, latino-americanas e internacionais relevantes ao público brasileiro: salas de imprensa e media centers de fabricantes; entidades públicas; confederações, federações, ligas e organizadores; prestadores oficiais de resultados; calendários; assessorias; redes sociais oficiais; imprensa especializada confiável; imprensa regional para descoberta de eventos; e mecanismos de busca para localizar fontes novas. A lista de fontes conhecida é ponto de partida, não universo fechado.
- Para notícias e lançamentos, revisar publicações recentes e páginas de imprensa, inclusive atualizações das últimas 72 horas que possam ter sido perdidas. Para eventos e competições, procurar itens novos e mudanças futuras em calendários, não apenas páginas já cadastradas. Para resultados, percorrer documentos, PDFs, planilhas, APIs e plataformas oficiais vinculadas.
- Em cada varredura geral, executar também o radar brasileiro de datas: ontem, hoje, próximos 7 dias e visão de 45 dias. Confirmar datas comemorativas, campanhas, semanas temáticas, efemérides, aniversários, marcos esportivos e oportunidades sazonais em fonte confiável. O dia anterior é obrigatório para recuperação de uma data relevante perdida enquanto ainda houver valor jornalístico.
- O **Dia do Motociclista no Brasil, 27 de julho**, é pauta anual obrigatória. Deve ser preparado com antecedência e publicado na data; se for perdido, deve entrar na primeira recuperação editorial útil, com contexto verdadeiro de retomada, sem fingir publicação no dia anterior.
- A pesquisa não termina ao encontrar o primeiro item. Manter uma fila editorial única com `descoberto`, `em_apuracao`, `publicavel`, `publicado`, `atualizado`, `duplicado`, `descartado_com_motivo` ou `bloqueio_externo`. Registrar fonte, horário, prioridade, destino editorial e motivo de qualquer descarte.
- Toda pauta `publicavel` deve ser criada ou atualizada no portal. Se o volume ultrapassar o tempo técnico de uma ocorrência, publicar primeiro urgências, segurança, recalls, resultados, mudanças de serviço e fatos com janela curta; deixar o restante como backlog executável para a próxima recuperação. Falta de tempo não transforma pauta válida em “sem novidade” e não permite apagar ou esquecer a fila.
- A prioridade organiza a ordem, mas não reduz a cobertura. Relevância baixa pode impedir uma matéria T+1 automática, porém nunca impede cadastrar ou atualizar corretamente evento, calendário, resultado ou serviço confirmado.
- O worker deve preferir atualização da página canônica quando já existir conteúdo sobre o mesmo assunto. Criar nova matéria quando houver fato novo, lançamento, mudança material, análise, contexto ou interesse jornalístico próprio. Não produzir duplicatas para aumentar volume.
- Qualidade, confirmação factual, direitos de imagem, não repetição, SEO e validação continuam obrigatórios. “Sem limite” significa sem teto de quantidade, não autorização para rumor, texto superficial, imagem sem direito ou conteúdo duplicado.

## Regra absoluta de não repetição de imagens e vídeos

- É proibido repetir em uma nova publicação qualquer imagem ou vídeo já usado no portal, na Revista, na TV, em programas, competições, eventos, capas, corpo de matéria, redes sociais ou outro conteúdo da TVDUASRODAS. A proibição vale tanto para arquivos idênticos quanto para cópias renomeadas, recomprimidas, recortadas, redimensionadas, convertidas para outro formato ou visualmente equivalentes.
- A regra inclui material de sites e fontes oficiais, bancos de imprensa, acervo próprio, capturas, ilustrações e imagens geradas por inteligência artificial. Uma imagem gerada por IA para uma publicação não pode ser reaproveitada em outra, mesmo quando o assunto for parecido.
- A imagem de capa nunca pode ser repetida dentro do corpo da mesma página. Cada posição visual deve usar um arquivo e uma composição distintos.
- Antes de selecionar ou publicar mídia, pesquisar todas as referências existentes em `content/news`, `content/videos`, `content/competitions`, `content/events`, `content/articles`, saídas sociais e demais coleções; comparar nome, URL, ID de vídeo, hash do arquivo e semelhança visual. Havendo dúvida razoável de repetição, rejeitar a mídia e escolher outra.
- Para notícias, resultados, lançamentos, programas e eventos em andamento, usar o material mais recente disponível e diretamente relacionado ao fato, à etapa, ao produto, ao local e à data cobertos. É proibido usar foto genérica ou antiga de modo que pareça retratar o acontecimento atual.
- As únicas exceções são retrospectivas claramente identificadas ou referências editoriais explícitas a artigo, notícia, vídeo ou acontecimento do passado. Nesses casos, a legenda e o texto devem informar que se trata de arquivo, incluir a data ou o contexto original e apontar o conteúdo anterior relacionado. A exceção deve ser registrada no relatório da execução.
- Se não houver mídia oficial atual, autorizada e inédita suficiente, documentar a busca e produzir uma solução visual nova e honesta, como ilustração editorial exclusiva ou gráfico baseado em dados confirmados. Nunca preencher espaço repetindo uma imagem.
- A validação anterior ao commit deve confirmar: nenhuma capa repetida no corpo; nenhuma mídia já usada em outra publicação; créditos e direitos corretos; atualidade e correspondência factual; carregamento local; e ausência de cópias visuais disfarçadas por nome, corte ou formato.

### Rotação semanal de matérias

- Toda matéria própria deve usar `contentType: "article"` e uma categoria ainda não usada por outra matéria própria na mesma semana, de segunda a domingo.
- Se uma matéria própria da categoria Cross já foi publicada naquela semana, a próxima matéria própria deve usar outra categoria.
- Notícias factuais usam `contentType: "news"` e podem repetir categoria quando houver novidade real, desdobramento ou atualização verificável.
- Edições de programa usam `contentType: "program"` e não participam da contagem da matéria diária nem da rotação de categorias das matérias próprias.
- Notícia cujo conteúdo principal seja agenda, serviço ou programação deve ir para Eventos. Resultado, classificação, etapa, liderança ou calendário esportivo deve atualizar Competições. Só publicar também na Revista quando existir uma reportagem editorial própria, com contexto e valor além da atualização estrutural.

## Diversidade temática obrigatória e proibição de repetição editorial

- Segurança é um pilar, não o tema padrão de toda matéria. É proibido escolher segurança apenas porque a busca de pauta foi insuficiente. A produção deve circular continuamente por famílias editoriais diferentes e refletir a amplitude do universo de duas rodas.
- Antes de escolher uma matéria própria, comparar todo o acervo, e não apenas a semana atual. Criar uma impressão digital editorial com assunto central, pergunta respondida, público, veículo/modalidade, recorte, conclusão principal e formato. Uma troca superficial de título, exemplos ou palavras não torna o tema novo.
- Não repetir matéria com a mesma pergunta central, explicação, lista, recomendação ou conclusão já publicada. Repetição só é permitida por pedido expresso de Wesley ou quando existir notícia em alta, mudança legal, novo produto, novo dado, nova ocorrência, atualização técnica ou desdobramento material verificável. Nesse caso, apresentar claramente o fato novo, atualizar ou linkar o conteúdo anterior e evitar recontar o texto antigo.
- Não publicar duas matérias próprias consecutivas da mesma família editorial. Em uma janela móvel de sete matérias próprias, buscar sete famílias ou recortes materialmente diferentes. Segurança preventiva genérica não pode ocupar mais de uma dessas sete posições; notícias factuais de acidente, recall ou emergência não contam como repetição quando tiverem fatos e análise próprios.
- A fila de pautas deve manter diversidade entre, no mínimo: lançamentos; mercado e indústria; custo de propriedade; compra, venda e financiamento; seguros; legislação e documentação; mecânica e diagnóstico; tecnologia e conectividade; elétricos e baterias; acessórios e equipamentos; design e engenharia; história e clássicas; cultura motociclista e ciclista; personagens e profissões; motoclubes e comunidades; turismo, rotas e hospedagem; mobilidade e urbanismo; infraestrutura e estacionamento; roubos e recuperação; competições e bastidores; eventos; bicicletas e modalidades; sustentabilidade; logística e trabalho; customização; comparativos baseados em dados; manutenção; formação; acessibilidade; comportamento; dados públicos; e serviço ao consumidor.
- A pauta própria do dia deve ser escolhida entre os maiores espaços de cobertura do acervo recente. Registrar quais foram as últimas 14 matérias próprias, suas famílias e perguntas centrais, e explicar internamente por que a nova pauta não repete nenhuma delas.
- Se houver várias notícias do mesmo tema em alta, todas podem ser publicadas como `contentType: "news"` quando cada uma tiver fato próprio. Isso não autoriza transformar todas as matérias próprias da semana no mesmo assunto.

## Cobertura responsável de acidentes e serviço completo ao leitor

- Em cada varredura geral, procurar acidentes recentes nas fontes oficiais de polícia, bombeiros, órgãos rodoviários, prefeituras, concessionárias, autoridades de trânsito e investigação, complementadas por imprensa local ou especializada confiável. Redes sociais servem para descoberta e evidência visual, nunca como única base para afirmar causa, culpa, morte, lesão, identidade ou responsabilidade.
- Publicar matéria quando houver informação verificável e valor público. Evitar sensacionalismo, imagens gráficas, exposição desnecessária de vítimas, menores, placas, documentos, prontuários, endereços particulares e dados pessoais. Não culpar vítima, condutor, fabricante, via ou terceiro sem conclusão oficial ou evidência técnica suficiente.
- Separar rigorosamente: `fato confirmado`, `informação preliminar`, `hipótese ainda investigada`, `fator de risco geral` e `orientação editorial`. Nunca transformar correlação, comentário de testemunha ou aparência da foto em causa comprovada.
- A matéria deve responder, conforme o caso e com fontes atuais:
  1. o que aconteceu, onde, quando, quais veículos estavam envolvidos e o que as autoridades confirmaram;
  2. o que ainda não foi esclarecido e qual órgão investiga;
  3. cadeia possível do acidente — via, sinalização, visibilidade, clima, velocidade, distância, treinamento, comportamento, manutenção, pneu, freio, iluminação, carga, capacete, equipamento, projeto ou falha mecânica — sem inventar causalidade;
  4. onde pode ter surgido o erro inicial e quais barreiras poderiam interromper a sequência;
  5. como reduzir o risco de ocorrência semelhante, distinguindo dever legal, boa prática e recomendação técnica;
  6. o que fazer imediatamente: proteger a área sem criar outro risco, acionar o serviço correto, não movimentar ferido salvo perigo iminente conforme orientação oficial, preservar provas e cooperar com o atendimento;
  7. o que sobreviventes, familiares e testemunhas devem documentar depois: atendimento médico, boletim ou registro equivalente, fotos permitidas, contatos, laudos, recibos, afastamento, reparos e comunicação à seguradora;
  8. seguro aplicável, coberturas contratadas, franquia, terceiros, APP, responsabilidade civil, perda parcial ou integral, despesas, prazos, documentos, preservação do salvado e riscos excluídos, sempre conferidos na apólice e em fonte oficial atual;
  9. prejuízo financeiro: veículo, equipamentos, remoção, oficina, transporte, renda interrompida, tratamento e demais perdas comprováveis, sem prometer indenização;
  10. onde reclamar ou reportar: órgão responsável pela via, autoridade policial ou de trânsito, seguradora e ouvidoria, `Consumidor.gov.br`, SUSEP, Procon, fabricante, concessionária ou canal de recall, conforme o problema e a jurisdição;
  11. direitos e próximos passos de sobreviventes e familiares, incluindo saúde física e mental, reabilitação, trabalho e previdência quando aplicável, usando somente orientação oficial atual e recomendando profissional habilitado para caso individual;
  12. correções sistêmicas possíveis para via, fiscalização, produto, manutenção, treinamento, comunicação e atendimento.
- Telefones, indenizações obrigatórias, DPVAT/SPVAT, prazos de seguro, prescrição, regras de trânsito, benefícios, procedimentos policiais e canais de reclamação mudam. Verificar a situação vigente na data da matéria em fonte oficial; nunca copiar orientação antiga nem apresentar aconselhamento jurídico ou médico individual como certeza.
- Para causas técnicas, procurar boletim de ocorrência quando público, laudo, nota da autoridade, recall, manual, norma, comunicado do fabricante, dados da via e especialista identificável. Se a investigação não terminou, publicar serviço preventivo sem fechar diagnóstico.
- Atualizar a matéria quando surgir laudo, identificação de causa, correção da via, recall, decisão da seguradora, conclusão policial ou outro desdobramento material. A atualização factual de um acidente já publicado deve preservar histórico e informar data e conteúdo da mudança.

## Uso de fotografias da internet e de contas sociais

- Uma fotografia estar acessível na internet ou em conta pública do Instagram não significa domínio público nem licença automática para republicação. Crédito e link são obrigatórios, mas não substituem autorização do titular dos direitos autorais e, quando aplicável, das pessoas retratadas.
- Fotos de Instagram podem ser usadas quando forem publicadas pelo próprio titular e a conta conceder permissão verificável à TVDUASRODAS, quando houver licença expressa compatível, quando forem fornecidas por assessoria/órgão oficial com uso editorial autorizado ou quando outra base legal aplicável tiver sido verificada. Guardar prova da autorização, licença, mensagem, termos ou política de uso no registro de fontes.
- O crédito de foto social deve aparecer junto da imagem no formato `Foto: Nome do fotógrafo — @perfil/Instagram`, com link para a publicação original. Se o fotógrafo não for identificado, usar `Foto: @perfil/Instagram`, sem atribuir autoria ao perfil como certeza. Identificar também o órgão, equipe, fabricante ou organizador quando pertinente.
- Se a conta republicou foto de terceiro, a autorização deve vir do fotógrafo ou titular real, não apenas do perfil que fez o repost. Marcação, hashtag, conta pública, compartilhamento, envio por seguidor ou presença de botão de compartilhar não concedem licença automática ao portal.
- É proibido remover marca-d’água, recortar crédito, baixar por método que contorne bloqueio, reutilizar foto de vítima sem avaliação ética ou usar captura de tela para contornar a falta de autorização.
- Em acidente, preferir imagem oficial autorizada da autoridade, concessionária, equipe de resgate ou fonte jornalística licenciada. Quando não houver fotografia documental licenciada, usar mapa, diagrama original, imagem da infraestrutura obtida legalmente ou ilustração claramente identificada, sem fabricar a cena real.

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

### Separação obrigatória entre auditoria interna e página pública

- URLs pesquisadas, quantidade de fontes ou domínios, tipo e peso de cada fonte, campos sustentados, horário da checagem, estado da busca, critérios de confiança, processamento visual/OCR, divergências, tentativas sem resultado e a estratégia de classificação pertencem exclusivamente ao controle interno.
- É proibido renderizar nas páginas públicas blocos como `Fontes cruzadas e atualização`, `Fonte e atualização`, `Verificação ainda aberta`, contagem de links/domínios, rótulos como `fonte específica independente` ou explicações sobre busca textual, visual, social e automatizada.
- A página pública deve mostrar somente informações úteis ao visitante: descrição do evento, datas, horários, endereço, programação, acesso, estacionamento, organização, resultados, classificações e um link direto para o canal oficial quando ele for útil.
- Quando um dado não estiver confirmado, comunicar apenas o estado público objetivo, como `Horário ainda não divulgado` ou `Estacionamento ainda não informado pela organização`, sem revelar o método de pesquisa.
- Os campos `sources`, `source_checked_at`, `research_status`, `visual_verification`, relatórios em `content/research` e demais evidências continuam preservados para auditoria e automação, mas nunca devem ser transformados em conteúdo visível, metadados descritivos ou texto indexável.
- Antes de publicar, `scripts/validate_project.py` deve reprovar qualquer página gerada de evento ou competição que exponha esses marcadores internos.

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
- É proibido omitir categoria, gênero, faixa etária, classe técnica ou divisão prevista no regulamento oficial, ainda que seja considerada secundária, tenha pouca participação ou menor apelo editorial. Antes de publicar, criar o inventário completo das categorias a partir do regulamento e conferir cada uma contra inscrições, largadas e resultados.
- Toda categoria deve permanecer visível com situação verificável: `agendada`, `em andamento`, `resultado provisório`, `resultado final`, `sem inscritos`, `não disputada` ou `cancelada`, conforme a fonte. A ausência momentânea de tabela não autoriza retirar a categoria nem inventar classificação.
- Quando o regulamento reunir categorias etárias em uma única disputa, explicar expressamente a unificação e reproduzir as duas informações: as categorias de origem e o nome oficial da classificação conjunta. Uma classificação conjunta oficial não pode ser apresentada como se as demais categorias tivessem sido esquecidas.
- Reproduzir a classificação oficial completa de cada categoria, incluindo todos os classificados e os estados `DNF`, `DNS`, `DSQ` e equivalentes quando constarem do documento. Pódio, Elite ou categoria principal nunca substituem a tabela completa.
- Em campeonatos, copas, torneios, ligas e circuitos por etapas, atualizar simultaneamente o resultado completo da etapa/rodada e a classificação geral acumulada de todas as categorias. Se a competição for de evento único e não possuir geral separada, declarar isso de forma explícita. Ranking federativo externo não deve ser confundido com a classificação geral do torneio.
- A página só pode ser considerada atualizada depois da conferência de todas as categorias e das duas camadas aplicáveis — etapa e geral — com data e horário da checagem. Uma atualização parcial deve ser identificada como parcial e continuar pendente nas janelas seguintes.
- Em divergência, preservar o dado anterior, registrar as versões conflitantes e procurar regulamento, júri, boletim ou documento posterior. A fonte mais recente e com autoridade direta prevalece.
- Antes de declarar ausência de dados, registrar no controle editorial quais camadas foram consultadas, URLs, data e horário. “Sem publicação” só é um estado válido depois dessa busca ampliada.

## Descoberta obrigatória de eventos ainda não cadastrados

- A cobertura não pode se limitar aos itens já presentes no portal. Nas janelas de 08h e 17h e nas auditorias de recuperação, pesquisar calendários nacionais e internacionais de motociclismo, ciclismo, MTB, BMX, estrada, pista, paraciclismo, motocross, supercross, arena cross, enduro, hard enduro, rally, rally raid, baja, trial, motovelocidade, scooter, e-bike, mobilidade, encontros, festivais, feiras, salões e demais modalidades relacionadas às duas rodas.
- Cruzar calendários de confederações, federações, ligas, organizadores, circuitos, plataformas oficiais contratadas e veículos especializados confiáveis. Verificar Brasil, América Latina e competições internacionais relevantes ao público brasileiro.
- Ao localizar evento confirmado ainda não cadastrado, criar ou atualizar imediatamente a página estrutural, calendário, datas, modalidade, local, fonte e situação. Não esperar o evento começar para cadastrá-lo.
- Eventos e competições descobertos depois da abertura entram imediatamente no fluxo de recuperação: cadastrar, corrigir data, hora local, fuso e situação, incorporar resultados/classificação já disponíveis e calcular o IRT. Coberturas de abertura e encerramento são recuperadas somente quando o item for `alta_relevancia`, sem duplicação.

## Enriquecimento profundo e inspeção visual de todos os eventos

- Em cada ocorrência das 08h e 17h, executar também `python scripts/audit_source_depth.py --output output/source-depth-daily.json --quiet`. Cada registro canônico deve buscar no mínimo duas fontes específicas, preferencialmente de domínios independentes, e ao menos uma fonte primária quando houver canal oficial publicado.
- Para os registros apontados pelo relatório, executar as estratégias de `scripts/research_all_events.py` por título/data, canal social e contato/organizador/local. A pesquisa deve continuar diariamente mesmo depois de uma tentativa sem resultado, porque novas páginas, regulamentos e publicações podem surgir.
- Resultado de busca só pode ser associado ao registro quando combinar a cidade e a identidade distintiva do evento ou do organizador. Palavras genéricas como `Motofest`, `encontro`, `moto`, `festival`, `solidário`, `aniversário` ou uma sigla curta não comprovam relação. Antes de publicar, executar `python scripts/prune_weak_indexed_sources.py --apply`.
- Quando existirem variações de grafia, UF, cidade ou título para o mesmo evento/data, executar `python scripts/canonicalize_duplicate_events.py`: manter uma página canônica completa, transferir as fontes úteis e gerar redirecionamento das rotas alternativas. Nunca apagar uma rota pública sem redirecionamento.
- Se, depois das três estratégias e da inspeção visual, nenhuma segunda fonte pública específica existir, não inventar nem usar homônimo. Manter o registro na fila diária, publicar somente os fatos legíveis no material disponível e declarar objetivamente os itens ainda não divulgados.
- Uma página de evento não é considerada completa apenas com nome, cidade e data. Cada ocorrência editorial das 08h e 17h e cada recuperação deve executar `python scripts/audit_event_completeness.py`, trabalhar a fila por prioridade e enriquecer os registros progressivamente até eliminar o backlog.
- Priorizar nesta ordem: eventos em andamento; encerrados nos últimos sete dias; começando nos próximos sete dias; começando nos próximos 30 dias; demais eventos futuros; acervo passado. Dentro da mesma janela, tratar primeiro a menor pontuação de completude e os possíveis duplicados.
- Para cada evento, pesquisar o organizador, prefeitura, entidade, moto clube, local, venda de ingressos, redes sociais e fontes comunitárias confiáveis. A busca textual deve ser acompanhada por **inspeção visual obrigatória** de flyers, cartazes, cards, carrosséis, mapas e imagens anexadas quando esses materiais existirem, porque horário, endereço e programação podem estar apenas na arte.
- A inspeção visual deve transcrever somente o que estiver legível e identificar a origem. Registrar `visual_verification` com tipo de material, URL, horário da checagem e campos confirmados. Texto extraído automaticamente deve ser conferido visualmente antes da publicação; logotipos, rostos ou inferências de layout não podem ser apresentados como fatos sem confirmação.
- O registro completo deve buscar e exibir, quando aplicável: `timezone`, `local_start`, `local_end` ou indicação de término não informado; nome do local; rua, número, bairro, cidade, estado e CEP; mapa ou referência de acesso; situação atual; organização e contato; ingresso ou gratuidade; estacionamento; camping; acessibilidade; classificação etária; regras de entrada; programação diária; atrações musicais; praça de alimentação; expositores, peças e acessórios; serviços para motociclistas e ciclistas; apoio institucional; e canais para alterações.
- Ausência de informação depois da busca não autoriza campo vazio nem suposição. Mostrar objetivamente `Não informado no material consultado` para acesso, estacionamento, camping, acessibilidade, classificação etária ou serviço não localizado. `free: false` não prova evento pago; usar `admission_status` para distinguir pago, gratuito e não informado.
- O endereço completo e o horário local devem aparecer nos cartões de serviço da página e no schema `Event`. A página deve exibir também acesso, estacionamento e organização quando disponíveis. O status do schema deve refletir `agendada`, `concluida`, `adiada` ou `cancelada`, sem manter evento passado como agendado.
- Fontes agregadoras servem para descoberta, mas a página deve substituir a fonte genérica por uma URL específica do evento assim que um flyer, publicação do organizador ou página oficial for localizada. Preservar a fonte anterior no histórico quando necessário.
- Detectar duplicidade por título normalizado, cidade, estado e data. Confirmar visualmente antes de consolidar; depois usar um único registro canônico, marcar os redundantes com `duplicate_of` e remover as páginas duplicadas do índice e do sitemap.
- Nenhum evento novo pode ser publicado com o texto genérico de agenda sem antes procurar endereço, horário, programação, acesso e fonte visual. Se a pesquisa realmente não localizar os dados, a página deve declarar quais itens continuam não informados, registrar as fontes consultadas e permanecer na fila de enriquecimento.

## Atualização universal e cobertura seletiva de abertura e encerramento

A atualização estrutural vale para **todos os eventos e todas as competições** cadastrados, nacionais ou internacionais, inclusive festivais, feiras, encontros, campeonatos, etapas e rodadas de vários dias. A cobertura editorial T+1 vale somente para itens classificados como `alta_relevancia`.

1. Em toda ocorrência editorial, comparar a data e hora atuais com `local_start` e `local_end` no `timezone` do evento, conferir o canal oficial e atualizar a situação estrutural:
   - Eventos: `agendada` antes da abertura, `em_andamento` entre início e fim, `concluida` depois do último dia, `adiada` quando confirmado e `cancelada` somente com confirmação oficial.
   - Competições/campeonatos: `agendada` antes do início, `em_andamento` durante a temporada ou etapa, `concluida` depois do encerramento e `cancelado` somente com confirmação oficial. Aplicar o mesmo controle a cada item de `rounds`.
   - Adiamento, mudança de data ou interrupção devem atualizar imediatamente datas, resumo, calendário e fonte oficial; nunca tratar ausência de notícia como cancelamento.
2. Quando `coverage_t1_required` for verdadeiro, no **dia seguinte ao primeiro dia** publicar uma notícia original na Revista explicando como foi a abertura. A matéria deve usar fonte oficial publicada depois da abertura, registrar fatos confirmados, destaques, serviço para os dias restantes e linkar a página estrutural do evento ou campeonato.
3. Quando `coverage_t1_required` for verdadeiro, no **dia seguinte ao último dia** publicar uma matéria de balanço completo: principais acontecimentos, resultados ou atrações, vencedores e classificação quando houver, números oficiais disponíveis, contexto e próximos passos. Atualizar a página estrutural para `concluida` no mesmo lote.
4. Em competição ou evento de **um único dia** e alta relevância, a matéria publicada no dia seguinte deve ser um balanço completo único e cumprir simultaneamente as coberturas de abertura e encerramento; não criar dois textos artificiais sobre o mesmo fato.
5. Em competições por etapas, calcular o IRT também para a etapa/rodada. A cobertura T+1 se aplica somente às etapas classificadas como `alta_relevancia`; a página da temporada permanece `em_andamento` enquanto houver etapa futura confirmada.
6. Não declarar presença da TVDUASRODAS, público, resultado, ocorrência, show realizado ou experiência presencial sem confirmação. Quando a primeira fonte consultada ainda não tiver publicado o balanço necessário, percorrer toda a matriz de fontes confiáveis. Só depois dessa busca ampliada registrar a obrigação como monitoramento externo; refazer a busca nas janelas seguintes e publicar assim que houver confirmação suficiente.
7. Antes de criar a matéria, verificar duplicidade por evento, competição, etapa, data e tipo de balanço. Registrar a cobertura na página estrutural ou no controle editorial para impedir publicação duplicada.
8. Cada notícia de abertura ou encerramento é conteúdo novo elegível para um Story e um Reel na próxima ocorrência da automação do Instagram, seguindo a regra de apenas uma publicação por formato e sem Feed.

## SEO imediato após cada publicação

Toda criação ou alteração pública deve encerrar o próprio ciclo de SEO antes de a execução seguir para outra pauta. Não esperar 20h.

1. Preparar SEO completo, executar `python scripts/build_seo_site.py`, depois `python scripts/update_sitemap.py` e `python scripts/update_sitemap.py --check`. O gerador é obrigatório após qualquer inclusão ou alteração em matérias, vídeos, competições, eventos, resultados, marcas ou modalidades. Ele deve manter `sitemap.xml` sem datas futuras e gerar `news-sitemap.xml` somente com matérias publicadas nas últimas 48 horas.
2. Fazer commit e push do lote.
3. Confirmar no domínio público a página alterada, `sitemap.xml` e `news-sitemap.xml`.
4. O workflow `.github/workflows/search-console.yml` deve reenviar automaticamente os dois sitemaps pela API do Search Console depois do push e atualizar `editorial/search-console/status.json`. A credencial técnica é a conta de serviço `tvduasrodas-search-console@involuted-reach-503620-p8.iam.gserviceaccount.com`, autorizada na propriedade exclusivamente por `tvduasrodas@gmail.com` e acessada pelo GitHub Actions com Workload Identity Federation, sem chave JSON permanente. O acesso federado deve permanecer restrito ao repositório `tvduasrodas/tvduasrodas`; se a automação falhar, fazer o reenvio manual usando somente `tvduasrodas@gmail.com`.
5. Para cada URL nova, solicitar indexação imediatamente após a publicação pública.
6. Registrar os estados corretos: `sitemap reenviado`, `indexação solicitada`, `indexada` ou `pendente`. Nunca chamar uma solicitação de indexação concluída. A URL Inspection API serve somente para acompanhar o estado; a Google Indexing API não deve ser usada.
7. Se push, acesso público ou Search Console falhar, registrar a pendência e aplicar a recuperação prevista neste documento; não adiar silenciosamente até 20h.

A auditoria das 20h é uma camada adicional de segurança para localizar qualquer SEO pendente do dia. Ela não substitui o SEO imediato de cada lote.

## Instagram — somente Reels e Stories

- A automação `Instagram TVDUASRODAS — Reels e Stories` executa diariamente às **08h30, 11h30, 14h30, 17h30 e 20h30**, em `America/New_York`, depois das janelas editoriais principais.
- O Instagram tem limite editorial absoluto de **cinco pautas por dia**, uma pauta no máximo em cada horário programado. Cada pauta escolhida gera somente **um Reel** e **um Story** coordenados sobre o mesmo assunto. Portanto, o teto diário é cinco assuntos, cinco Reels e cinco Stories; nunca cinco de cada formato sobre assuntos diferentes.
- O limite de cinco vale para publicações novas e recuperações combinadas. A recuperação pode concluir um Story ou Reel falho da mesma pauta sem contar assunto novo, mas nunca pode introduzir uma sexta pauta no mesmo dia.
- Todo conteúdo novo ou materialmente atualizado no portal entra como candidato, não como publicação social automática. Manter uma fila diária de candidatos e, em cada horário, recalcular a importância com base em urgência, segurança, alcance, interesse brasileiro, novidade, atualidade, impacto esportivo ou de serviço e qualidade da mídia disponível.
- Publicar em cada horário apenas a pauta elegível de maior importância ainda não usada naquele dia. Não selecionar simplesmente o primeiro conteúdo novo. Se não existir pauta forte, mídia autorizada e condições técnicas suficientes, não preencher a vaga com conteúdo fraco; registrar a janela sem publicação. Uma vaga não utilizada não autoriza ultrapassar cinco pautas em outro horário.
- Efemérides diretamente ligadas ao canal, recalls, alertas de segurança, grandes lançamentos, resultados relevantes e mudanças urgentes de evento devem disputar prioridade com as demais pautas do dia. O radar de datas encaminha candidatos, mas somente esta automação decide e publica dentro do teto diário.
- É proibido criar, agendar ou publicar posts de Feed, fotografias no grid ou carrosséis. A opção `Create post` do Meta Business Suite não deve ser usada.
- O Feed existente deve ser preservado. Não excluir publicações antigas. Registros antigos com Feed são apenas histórico e não autorizam repetição.
- Para novos registros em `output/instagram/publication-log.json`, omitir o campo de Feed ou registrar `NAO_APLICAVEL_POR_REGRA`, sem gerar arquivo ou publicação para o Feed.
- Stories devem usar formato vertical `1080x1920`, vídeo MP4 de 12 a 15 segundos, H.264 com áudio AAC e trilha original ou comprovadamente licenciada.
- Reels devem usar formato vertical `1080x1920`, MP4 H.264 com áudio AAC, preferencialmente entre 20 e 35 segundos, gancho nos primeiros dois segundos, **5 a 7 cenas**, textos dentro da área segura, capa legível e CTA para seguir `@tvduasrodasofc` e acessar `TVDUASRODAS.COM`.
- O desenho aprovado é obrigatório em todos os Reels: fotografia ou imagem editorial dominante, tipografia forte e quatro blocos independentes — (1) contexto em caixa laranja, (2) título em caixa escura própria, (3) informação complementar em outra caixa escura própria e (4) crédito fotográfico separado. É proibido usar layer preto integral, tarja única cobrindo grande parte da imagem ou texto sem fundo que perca legibilidade.
- Todo Reel deve ser um slideshow de **pelo menos cinco imagens realmente diferentes**. Repetir o mesmo arquivo, usar outro corte da mesma foto, espelhar, ampliar ou alterar cor não conta como imagem diferente. A automação deve comparar os arquivos e interromper a publicação quando detectar repetição ou quando houver menos de cinco imagens elegíveis.
- Em atualizações sobre como foi um evento ou competição, usar somente fotografias reais daquela edição, etapa ou dia, obtidas de fonte oficial ou acervo com autorização editorial. Não misturar imagens genéricas, de outra edição ou geradas por IA como se fossem registro documental. Cada foto deve ter fonte, crédito e direitos registrados.
- As transições entre cenas devem seguir o padrão `page peel` diagonal aprovado. A trilha padrão é rock instrumental original ou comprovadamente licenciada; música comercial sem licença continua proibida.
- Gerar os Reels padronizados com `python scripts/build_instagram_reel.py --manifest <manifesto.json> --output-dir <pasta>`. O manifesto deve confirmar `rights_verified: true`, conter de 5 a 7 cenas, indicar imagem local, contexto, título, informação, crédito e URL da fonte para cada cena. O gerador deve produzir `reel.mp4`, `reel-cover.jpg`, as cenas, as transições e `reel-build.json`; a publicação só pode prosseguir se o recibo confirmar no mínimo cinco hashes de imagem distintos.
- Não usar música comercial sem licença, não fabricar cenas documentais e não afirmar publicação sem confirmação visível na conta profissional `@tvduasrodasofc`.
- Usar obrigatoriamente `Create reel` para Reels e `Create story` para Stories. Nunca publicar o vídeo como post comum.
- Registrar separadamente, para cada Story e Reel: arquivo, duração, trilha, horário, destino, permalink ou identificador disponível e confirmação verdadeira da publicação.
- Todos os arquivos e registros criados pela automação do Instagram devem ser incluídos em commit e push para `origin/main` antes do encerramento. Se o push direto falhar, aplicar imediatamente a seção **Recuperação obrigatória de publicação** deste documento.
- A automação do Instagram não pode declarar conclusão com arquivos apenas locais, commit à frente de `origin/main` ou publicação sem confirmação.

### Limpeza obrigatória dos arquivos locais do Instagram após 24 horas

- Os arquivos de produção armazenados em subpastas de `output/instagram` são temporários. Depois de **24 horas completas** da publicação confirmada no Instagram, devem ser excluídos do computador e do repositório para liberar espaço. O prazo começa no horário mais recente entre Story, Reel e eventual Feed legado publicado.
- Executar `python scripts/cleanup_instagram_output.py --apply` em todas as ocorrências da automação do Instagram, depois de preservar o registro da publicação e antes do commit final. As automações de recuperação também devem executar ou recuperar essa limpeza quando houver pastas elegíveis.
- A exclusão só é permitida quando Story e Reel estiverem com `status: "PUBLICADO"`, `publishedAt` válido com fuso e confirmação por permalink, identificador da Meta ou mensagem de publicação. Feed legado, quando existir como `PUBLICADO`, deve cumprir os mesmos requisitos. Status pendente, falha, ausência de horário ou falta de confirmação bloqueiam a limpeza.
- O script deve operar primeiro em modo de simulação por padrão e aplicar exclusões somente com `--apply`. É proibido reduzir `--retention-hours` para menos de 24.
- A limpeza deve remover somente a pasta comum registrada para aquela publicação dentro de `output/instagram`. Nunca excluir `output/instagram` inteiro, `publication-log.json`, `design-review`, `source`, `assets/img/uploads`, conteúdo do portal, arquivos de fonte ou qualquer caminho fora da raiz permitida.
- Antes da exclusão, conferir o caminho absoluto, a quantidade de arquivos e o total de bytes. Pastas compartilhadas por mais de um registro, links simbólicos, caminhos ambíguos ou referências fora do escopo devem ser preservados e registrados como pendência.
- `output/instagram/publication-log.json` é histórico permanente e não deve ser apagado. Após cada limpeza, acrescentar ao registro `localCleanup` com situação, horário, pasta removida, retenção aplicada, quantidade de arquivos, bytes liberados e razão.
- As exclusões e a atualização de `publication-log.json` devem entrar no commit e no push da mesma ocorrência, para que os arquivos também deixem de ocupar espaço em `origin/main`. Confirmar `HEAD == origin/main` antes de declarar a limpeza concluída.
- Arquivos com menos de 24 horas, publicações sem `publishedAt`, mídia ainda necessária para nova tentativa e qualquer item sem confirmação visível devem permanecer intactos. A limpeza nunca pode apagar material para compensar falha de publicação.

## Grade fixa dos programas da Revista

Os programas funcionam como edições especiais em texto e fotos, publicadas separadamente da matéria diária. A grade deve ser cumprida sempre que o dia corresponder:

- **Rolê de Rua:** segundas e quintas — mobilidade, vida urbana, personagens, rotas curtas, scooters, motos e bicicletas na cidade.
- **Garage Tech:** quartas — mecânica, manutenção, componentes, ferramentas e tecnologia explicada.
- **Estrada Aberta:** sábados — rotas, turismo, preparação, segurança e histórias de viagem.
- **Electric Zone:** domingos — veículos elétricos, baterias, recarga, eletrônica, infraestrutura e mobilidade limpa.

### Formato soberano do Electric Zone

O **Electric Zone** é o programa técnico e educativo da TVDUASRODAS dedicado a veículos, componentes, dispositivos e acessórios elétricos ligados a motos, scooters, bicicletas, ciclomotores, mobilidade urbana e ao trabalho sobre duas rodas. Cada domingo deve apresentar uma descoberta nova e útil, com profundidade suficiente para que o leitor compreenda o sistema, avalie uma compra, reconheça sintomas e converse melhor com um profissional. O programa não é uma coleção de dicas genéricas de segurança.

Cada edição deve escolher **um objeto técnico central** — veículo, componente, módulo, ferramenta, carregador, conector, sensor, controlador, bateria, motor, conversor, acessório ou gadget — que ainda não tenha sido tratado com o mesmo recorte. Antes de produzir, comparar a pauta com todo o acervo do programa, registrar o que é realmente novo e evitar repetir título, explicação, exemplos, fotografias ou estrutura da edição anterior.

A edição deve conter, quando aplicável:

1. **Descoberta inicial:** uma situação humana ou sintoma reconhecível que revele por que o objeto importa para motociclistas, ciclistas, entregadores, oficinas, frotas ou usuários urbanos.
2. **Mapa do sistema:** diagrama original mostrando entrada, saída, conexões, proteções e relação do objeto com o restante do veículo.
3. **Princípio de funcionamento:** explicação acessível, tecnicamente correta e progressiva; termos técnicos devem ser definidos no primeiro uso.
4. **Ficha técnica comentada:** tensão, corrente, potência, eficiência, materiais, dimensões, interfaces, protocolos, proteção ambiental, temperatura, certificações e demais parâmetros relevantes, sempre explicando a consequência prática de cada número.
5. **Modelos e compatibilidade:** diferenças entre famílias, versões, anos, conectores e arquiteturas; nunca chamar uma peça de universal apenas porque duas tensões coincidem.
6. **Benefícios e limites:** o que o dispositivo resolve, o que não resolve e quais compromissos de custo, peso, autonomia, calor, durabilidade ou manutenção ele cria.
7. **Cuidados e manutenção:** inspeção, limpeza, armazenamento, sinais de desgaste e periodicidade, sem preencher a edição com conselhos genéricos.
8. **Diagnóstico orientado por sintomas:** sequência lógica de verificações, instrumentos necessários e critérios que diferenciem falha do componente, alimentação, chicote, comando e carga.
9. **Reparabilidade:** separar claramente o que o usuário pode verificar, o que uma oficina pode reparar e o que exige substituição, laboratório, isolamento ou assistência autorizada. Alta tensão, freios, estrutura e sistemas críticos sempre recebem limite profissional explícito.
10. **Como e onde comprar:** fabricante, concessionário, assistência, distribuidores técnicos, critérios contra falsificação, documentos a exigir e perguntas a fazer. Preço ou estoque só podem ser publicados após verificação atual.
11. **Conexão vertical:** pelo menos uma informação útil ligada ao tema, mas além do próprio objeto — infraestrutura urbana, pontos de recarga, rotina de motoboys, gestão de frota, logística reversa, ferramentas comunitárias, custo de energia, legislação, cursos, mapas ou serviços especializados.
12. **Aplicação coletiva:** mostrar como uma comunidade, oficina, associação ou grupo profissional pode padronizar, compartilhar, medir ou aprender com aquele conhecimento.
13. **Síntese de descoberta:** encerrar com três ou mais fatos que o leitor provavelmente não sabia antes da edição, sem repetir um checklist vazio.

Toda edição deve usar no mínimo duas fontes técnicas primárias ou oficiais, confrontar manuais de veículo com documentação do componente e distinguir dado do fabricante, cálculo editorial e exemplo hipotético. A pauta deve ter capa inédita e pelo menos duas imagens internas inéditas quando houver material adequado, incluindo obrigatoriamente um diagrama ou esquema original quando o assunto envolver fluxo de energia, sinal, montagem ou diagnóstico. Fotografias oficiais são prioritárias; ilustrações por IA só podem ser usadas quando não houver material oficial adequado e devem ser identificadas sem sugerir modelo, instalação ou ocorrência real.

O card do programa é parte obrigatória da publicação. Na Revista, a edição precisa manter a identidade visual de **Electric Zone** mesmo quando for escolhida como destaque principal: selo de programa, nome da série, domingo e indicação de edição semanal devem permanecer visíveis. Nenhuma edição pode aparecer como card comum apenas porque ocupa a posição de destaque.

São insuficientes e devem ser refeitas antes da publicação: listas superficiais, pautas sustentadas apenas por “dicas de segurança”, textos que apenas definem o componente, conteúdo semelhante a edições antigas, imagens recicladas, compra sem critérios técnicos, reparo sem limites profissionais, especificações sem consequência prática e matérias sem descoberta verificável.

Cada edição precisa ter `contentType: "program"`, capa horizontal, no mínimo duas imagens internas quando houver material oficial, texto aprofundado, fontes oficiais, links internos e campos `program`, `programLabel`, `episodeDuration` e `readingTime`. O título deve identificar a edição da semana de forma editorial, por exemplo `Rolê de Rua — edição de DD/MM/AAAA`, sem transformar essa identificação em texto burocrático. A duração planejada e qualquer estrutura de futuro programa em vídeo são informações internas: nunca publicar ao leitor marcações de minutos, bastidores ou avisos sobre um futuro TV Show. Em terças e sextas não há edição fixa, mas a matéria diária independente continua obrigatória.

Na capa da Revista, programas são uma categoria editorial permanente e prioritária, separada de matérias próprias e notícias. O bloco de programas deve aparecer antes do fluxo comum. Nos resultados da Revista, todo `contentType: "program"` deve usar card visualmente distinto, com identidade de série, nome do programa, dia da grade e indicação de edição semanal; não pode parecer um card comum que recebeu apenas outra etiqueta. Os filtros devem permitir separar `Programas`, `Matérias` e `Notícias`, além dos filtros temáticos. A diferenciação é editorial e visual; não altera a exigência de conteúdo aprofundado nem permite contar programa como matéria diária.

Conteúdo fraco, duplicado, rumor ou texto inventado não cumpre a meta. Quando não houver release forte, a matéria diária deve ser uma pauta própria útil e durável, sustentada por fontes técnicas ou oficiais.

## 08h — Radar editorial e notícias

- Ler a memória da execução anterior e rodar `python scripts/check_daily_targets.py`.
- Executar a varredura geral completa da seção **Redação permanente, descoberta geral e publicação sem teto**, incluindo o radar de ontem, hoje, próximos 7 dias e visão de 45 dias. Consultar fontes conhecidas e fazer busca aberta por fontes e fatos novos.
- Auditar data e hora locais, fuso, situação e sinais de relevância de todos os eventos, competições e rodadas. Publicar antes das pautas discricionárias qualquer matéria T+1 vencida dos itens `alta_relevancia`, além de corrigir `agendada`, `em_andamento`, `concluida`, `adiada` ou `cancelada` para todos, conforme fonte oficial.
- Fazer a **primeira verificação obrigatória de SEO do dia** com `python scripts/update_sitemap.py --check`.
- Conferir se o fechamento de SEO do dia anterior foi concluído: sitemap gerado depois da última publicação, enviado ao Google Search Console e URLs novas solicitadas para indexação. Se faltar qualquer etapa, corrigir, publicar e concluir usando somente `tvduasrodas@gmail.com` antes de seguir.
- Se o sitemap estiver desatualizado, executar `python scripts/update_sitemap.py`, validar a contagem por coleção, publicar e reenviar o sitemap no Search Console.
- Verificar salas de imprensa brasileiras e internacionais, fabricantes, Abraciclo, Fenabrave, recalls, órgãos públicos, CBM, CBC, entidades internacionais, áreas específicas de resultados/ranking, prestadores oficiais contratados, calendários monitorados, redes oficiais e imprensa especializada confiável. A memória incremental serve para evitar repetição, não para reduzir a amplitude da busca.
- Fazer descoberta ativa de eventos e competições ainda não cadastrados, seguindo a matriz de fontes; não limitar a auditoria ao acervo existente.
- Dar prioridade a recall, segurança, lançamento brasileiro, mudança de mercado, evento próximo e resultado urgente.
- Publicar todas as matérias, páginas e atualizações confirmadas e relevantes encontradas nesta janela. Agrupar em lotes seguros quando isso acelerar a execução, sem criar teto numérico.
- Não encerrar o dia nem considerar as metas cumpridas apenas porque competições não mudaram.

## 11h — TV e vídeos

- Antes da seleção de vídeo, atualizar fontes urgentes da varredura geral e publicar recalls, mudanças de serviço, lançamentos, resultados ou notícias confirmadas surgidas desde as 08h. Isso é adicional ao vídeo e não o substitui.
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
- Atualizar fontes urgentes e a fila editorial geral antes de produzir a pauta própria. Publicar também todas as notícias, lançamentos, efemérides ou atualizações confirmadas desde a janela anterior; elas não substituem a matéria independente nem o programa.
- Se não existir `contentType: "article"`, produzir obrigatoriamente a matéria diária, mesmo que já exista notícia ou edição de programa no dia.
- Conferir as últimas 14 matérias próprias, suas famílias, perguntas centrais e conclusões. Escolher uma família ainda não usada na semana e um tema materialmente inédito em todo o acervo; segurança não pode ser escolhida novamente como pauta genérica se já apareceu entre as últimas sete matérias próprias.
- Quando houver programa fixo no dia, produzir também uma edição separada com `contentType: "program"`. O programa não substitui a matéria diária e a matéria diária não substitui o programa.
- Quando não houver notícia ou lançamento forte, escolher a maior lacuna real do acervo entre mercado, indústria, custos, compra, seguro, legislação, mecânica, tecnologia, elétricos, design, história, cultura, personagens, profissões, motoclubes, turismo, infraestrutura, mobilidade, urbanização, bicicletas, modalidades, acessórios, logística, customização, dados, serviço ao consumidor e outras famílias da matriz de diversidade. Segurança é apenas uma opção e nunca o fallback automático.
- Usar texto original em pt-BR, sem copiar releases e sem afirmar teste presencial que não ocorreu.
- Priorizar capa oficial horizontal e duas imagens internas autorizadas, sempre atuais, distintas entre si e inéditas em todo o acervo publicado. Baixar, otimizar e publicar localmente; não usar hotlink. IA somente quando não houver material oficial adequado e sempre com geração exclusiva para a publicação, sem reaproveitamento.
- Registrar fontes, direitos, créditos e tratamento das imagens.
- Após cada lote publicado, concluir imediatamente sitemap, push, validação pública e Search Console.

## 17h — Competições, eventos e segunda rodada de notícias

- Reexecutar integralmente a varredura geral, sem se limitar a esportes e sem teto de publicações. Revisar novamente salas de imprensa, fabricantes, mercado, recalls, segurança, mobilidade, bicicletas, elétricos, eventos, efemérides e fatos descobertos pela imprensa especializada desde as 08h.
- Verificar resultados, pódios, pontos, liderança, etapas e calendários em todas as camadas da matriz de fontes confiáveis, incluindo PDFs, planilhas, APIs e prestadores oficiais em domínios externos.
- Repetir a auditoria universal de data, hora local, fuso e situação, atualizar o IRT e revisar alertas de crescimento. Para itens `alta_relevancia`, repetir a auditoria de matérias T+1. Se a primeira fonte de uma abertura ou encerramento ainda não estava disponível às 08h, pesquisar novamente em toda a matriz e publicar o balanço assim que houver confirmação suficiente.
- Atualizar páginas existentes e preservar histórico; não publicar apenas o vencedor quando a tabela oficial completa estiver disponível.
- Verificar eventos nacionais e internacionais relevantes ao público brasileiro e cadastrar os confirmados que ainda não existam no portal.
- Publicar todas as mudanças esportivas e todas as demais pautas confirmadas de produto, mercado, recall, segurança, mobilidade, ciclismo, eventos ou efemérides. A busca geral é obrigatória mesmo quando houver muitas mudanças esportivas; uma categoria não pode encerrar ou esconder as demais.

## 20h — Fechamento obrigatório e auditoria final de SEO

- Rodar `python scripts/check_daily_targets.py --require-complete`.
- Fazer a última atualização das fontes urgentes e revisar toda a fila editorial. Metas mínimas completas não encerram o dia enquanto houver pauta `publicavel` ou atualização material executável.
- Confirmar que nenhuma obrigação T+1 vencida de item `alta_relevancia` ficou sem publicação e que todos os eventos, campeonatos, etapas e rodadas, independentemente do porte, refletem data e hora locais, fuso, situação e comunicados oficiais.
- Se faltar matéria independente, vídeo elegível em pt-BR ou programa fixo do dia, produzir e publicar cada item pendente antes de encerrar, respeitando qualidade, fontes, diversidade e direitos.
- Publicar também todas as demais pautas executáveis do backlog. Se um bloqueio técnico real impedir terminar o volume no mesmo horário, preservar cada item com fonte, prioridade e próximo passo para a recuperação; nunca resumir o backlog como “sem novidade”.
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
**Diversidade editorial:** famílias e recortes das matérias próprias, comparação com as últimas 14 e confirmação de que não houve repetição temática.
**Acidentes e serviço:** ocorrências cobertas ou atualizadas, fontes oficiais, causa confirmada ou ainda investigada e orientações práticas incluídas.
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
4. Executar `python scripts/build_seo_site.py` para atualizar as páginas HTML canônicas, relações internas, entidades e o manifesto SEO.
5. Executar `python scripts/update_sitemap.py`.
6. Executar `python scripts/update_sitemap.py --check` e validar `sitemap.xml` e `news-sitemap.xml`, incluindo contagem `static + canonical_generated`, XML, URLs únicas, datas não futuras, janela de notícias de 48 horas e ausência de fragmentos inválidos como `#U` ou `%23U`.
7. Fazer commit apenas dos arquivos relacionados e push para `origin/main`.
8. Confirmar a URL, imagem, layout, `sitemap.xml` e `news-sitemap.xml` no domínio público.
9. Confirmar que o workflow do Search Console reenviou automaticamente os dois sitemaps e atualizou o painel. Em caso de falha, entrar somente como `tvduasrodas@gmail.com`, reenviar os dois sitemaps manualmente e solicitar indexação das URLs novas. Nunca usar `wesleyrodrigo29@gmail.com`.
10. Concluir os passos 1 a 9 imediatamente após o push. Não aguardar a execução das 20h; às 20h apenas auditar e corrigir pendências.

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
- Nunca repetir imagens ou vídeos, inclusive mídia de fonte oficial, acervo próprio ou gerada por IA; somente retrospectiva ou referência explícita ao passado pode usar arquivo, com identificação, data, contexto e link para o conteúdo anterior.
- Não deixar publicação válida somente no computador: validar, fazer commit, push e confirmar no site.
- A autorização permanente cobre commit, clique em `Push origin`, push para `origin/main` e confirmação remota de todos os lotes previstos por esta rotina. Não pedir nova autorização para essas ações.
- Toda execução gera relatório visível: checado sem novidade, publicado com URL ou ação necessária.
- CAPTCHA, 2FA, novo OAuth, pagamento ou nova permissão exigem Wesley; tarefas independentes continuam.
