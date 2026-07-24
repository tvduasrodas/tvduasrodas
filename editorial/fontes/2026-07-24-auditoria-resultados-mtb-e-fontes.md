# Auditoria de resultados e ampliação de fontes - 24/07/2026

## Correção imediata - Brasileiro de MTB 2026

- Entidade responsável: Confederação Brasileira de Ciclismo (CBC).
- Página de resultados consultada: https://www.cbc.esp.br/modalidades/resultados/busca/mtb
- Documento oficial do XCE: https://www.cbc.esp.br/arquivos/w7bd2d50zb.pdf
- Data do resultado: 23/07/2026.
- Arquivo de auditoria preservado em `editorial/fontes/brasileiro-mtb-2026-resultados/xce-resultados-2026-07-23.pdf`.
- O documento foi criado pela organização em 23/07/2026 e contém as classificações finais completas do XCE Elite Feminino e do XCE Elite Masculino.
- Conferência visual realizada após renderização da página única do PDF. Os nomes, equipes e posições publicados na página estrutural foram transcritos do documento, incluindo oito classificadas no feminino e nove classificados no masculino. O atleta masculino marcado como DNS não foi incluído entre os classificados.

## Falha identificada no processo anterior

A notícia oficial da abertura foi consultada, mas a área separada de resultados da CBC não foi incorporada à página estrutural. Isso produziu uma página com pódio no texto e `standings` vazio, embora o PDF oficial já estivesse disponível.

## Regra corretiva aplicada

A busca passa a percorrer uma matriz de fontes:

1. entidade reguladora ou organizador;
2. áreas específicas de resultados, ranking, documentos e anexos;
3. prestador oficial contratado em domínio externo;
4. fontes primárias complementares;
5. duas fontes secundárias confiáveis quando não houver documento primário disponível.

Uma consulta isolada à página principal ou à área de notícias não é suficiente para declarar ausência de resultado ou classificação.

