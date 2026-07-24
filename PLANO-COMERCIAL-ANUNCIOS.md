# Plano comercial de anúncios — TVDUASRODAS

Versão inicial: 24 de julho de 2026.

## Princípio do inventário

Todo anúncio deve corresponder ao assunto principal da página ou do vídeo. Conteúdo de motos recebe campanha de motos; bicicletas, scooters, elétricos, mobilidade, tecnologia, competições e eventos recebem suas respectivas campanhas. Se não houver campanha ativa para a categoria e o formato, entra somente a campanha institucional geral da TVDUASRODAS.

O catálogo central é `content/ads/config.json`. A troca de patrocinador ocorre nesse arquivo, nunca manualmente em uma matéria isolada. Uma campanha nova de Scooters, por exemplo, passa a valer em todas as matérias, programas, vídeos, competições e eventos classificados como Scooters.

## Formatos comerciais

| Código técnico | Nome comercial | Criação desktop | Uso principal |
|---|---|---:|---|
| `retangulo-lateral-300` | Retângulo Lateral 300 | 300 × 250 px | Topo da lateral de matéria ou vídeo |
| `faixa-editorial-728` | Faixa Editorial 728 | 728 × 90 px | Meio da matéria ou área contextual do vídeo |
| `billboard-cobertura-970` | Billboard de Cobertura 970 | 970 × 250 px | Competições, eventos e páginas especiais |

No celular, os três formatos ocupam a largura disponível e preservam a proporção e a legibilidade. A criação deve manter textos e logotipos dentro de uma área segura de 90% da largura e 80% da altura.

## Categorias vendáveis

- Motos
- Bicicletas
- Scooters
- Elétricos
- Mobilidade
- Tecnologia e manutenção
- Competições
- Eventos
- Geral/institucional

## Pacotes sugeridos para precificação futura

1. **Presença:** um formato e uma categoria.
2. **Contexto:** Retângulo Lateral 300 + Faixa Editorial 728 na mesma categoria.
3. **Cobertura:** Billboard de Cobertura 970 em competição ou evento, com período definido.
4. **Domínio de categoria:** todos os formatos disponíveis de uma categoria por período contratado.

Os preços devem considerar formato, categoria, período, exclusividade, quantidade estimada de impressões e prioridade da campanha. Nenhum valor está fixado nesta versão.

## Requisitos de cada campanha

- `id` único;
- situação `active` ou `inactive`;
- uma ou mais categorias;
- formatos contratados;
- data inicial e final quando houver;
- rótulo publicitário;
- título, descrição e CTA;
- URL de destino;
- imagem e texto alternativo quando o patrocinador fornecer criação própria.

Campanhas vencidas ou inativas não podem ser exibidas. É proibido misturar categorias apenas para preencher inventário.
