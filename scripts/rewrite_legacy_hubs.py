#!/usr/bin/env python3
"""Transforma quatro URLs legadas em hubs editoriais próprios e completos."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


HUBS = {
    "guia-scooters-eletricas.html": {
        "title": "Planejador de scooter elétrica urbana | TV Duas Rodas",
        "description": "Ferramenta editorial para comparar recarga, autonomia, garantia, assistência e custo total antes de escolher uma scooter elétrica.",
        "h1": "Planejador de scooter elétrica: recarga, autonomia e custo total",
        "tag": "Ferramenta editorial · Elétricos",
        "image": "/assets/img/uploads/scooters-eletricas-recarga-commons.webp",
        "image_alt": "Motocicletas e scooter elétricas estacionadas durante recarga",
        "image_caption": "Recarga de veículos elétricos de duas rodas. Foto: Charbel1719 / Wikimedia Commons, CC BY-SA 4.0.",
        "image_source": "https://commons.wikimedia.org/wiki/File:Recharge_des_motos_%C3%A9lectriques_Commando.jpg",
        "bad_video": "3GwjfUFyY6M",
        "body": """
                  <p class="article-update-note"><strong>Atualizado em 22 ago 2026.</strong> Esta página é um roteiro de decisão. O guia narrativo completo permanece em <a href="/guias/guia-scooters-eletricas/">Scooters elétricas na cidade</a>.</p>

                  <p>Comprar uma scooter elétrica exige confirmar mais do que a autonomia anunciada. A rotina de recarga, a instalação disponível, a garantia da bateria, a rede de assistência e a classificação do veículo determinam se a escolha funciona no dia a dia. Use os blocos abaixo como uma ficha de apuração: preencha apenas com documentos do modelo e propostas formais do vendedor.</p>

                  <h2>1. Identifique exatamente o veículo</h2>
                  <ul>
                    <li>Fabricante, modelo, versão e ano-modelo;</li>
                    <li>potência nominal, velocidade máxima declarada e tipo de homologação;</li>
                    <li>necessidade de registro, placa e habilitação, confirmada na documentação;</li>
                    <li>peso, capacidade de carga e limite para passageiro.</li>
                  </ul>
                  <p>Não use apenas o nome comercial. Veículos visualmente parecidos podem ter enquadramentos e obrigações diferentes. A <a href="https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-contran/resolucoes/Resolucao9962023.pdf" target="_blank" rel="noopener">Resolução Contran nº 996/2023</a> reúne definições atuais para ciclomotores, bicicletas elétricas e equipamentos autopropelidos; a confirmação do produto concreto deve vir do fabricante e dos órgãos de trânsito.</p>

                  <h2>2. Mapeie a recarga antes de olhar o preço</h2>
                  <p>Registre onde a scooter ficará à noite, se a tomada pertence à sua unidade, qual tensão e corrente o carregador exige e se o condomínio autoriza a instalação. Extensão improvisada, adaptador ou ponto sem avaliação elétrica não é plano de recarga. Peça o manual do carregador e, quando houver instalação fixa, consulte profissional habilitado.</p>
                  <ul>
                    <li><strong>Local principal:</strong> casa, garagem, trabalho ou estação autorizada;</li>
                    <li><strong>Plano alternativo:</strong> ponto disponível caso a recarga principal falhe;</li>
                    <li><strong>Bateria removível:</strong> peso, trava, limite de transporte e condições de armazenamento;</li>
                    <li><strong>Tempo:</strong> intervalo informado pelo fabricante para a tomada que você realmente possui.</li>
                  </ul>

                  <h2>3. Calcule autonomia com margem documentada</h2>
                  <p>Comece pela distância total do dia e acrescente desvios previsíveis. Depois solicite ao fabricante o ciclo usado na autonomia declarada: velocidade, carga, modo de condução e temperatura. Em vez de aplicar um desconto percentual genérico, faça um test ride autorizado no seu tipo de trajeto e registre o consumo de bateria. Subidas, velocidade, garupa, vento e temperatura alteram o resultado.</p>

                  <h2>4. Monte o custo total</h2>
                  <p>Some preço, financiamento, documentação, seguro, energia, pneus, freios, revisões, conectividade e eventual aluguel da bateria. Solicite por escrito o preço de reposição do conjunto de bateria, prazo de fornecimento, condições de garantia e critérios de perda de capacidade. Para estimar energia, use a capacidade efetivamente reposta em kWh e a tarifa da sua conta; não copie valores médios de outra cidade.</p>

                  <h2>5. Teste assistência e pós-venda</h2>
                  <p>Ligue para a oficina indicada antes da compra. Pergunte quem executa diagnóstico do sistema de alta tensão, quais peças ficam em estoque, como funciona o reboque e qual o prazo médio de atendimento. Confira no contrato quem responde pela bateria e pelo carregador. Guarde proposta, manual e condições de garantia.</p>

                  <h2>Decisão final</h2>
                  <p>A scooter deve atender percurso, carga, recarga e orçamento ao mesmo tempo. Se um desses quatro pontos depender de promessa verbal, a decisão ainda não está pronta. Compare sua ficha com a <a href="/materias/scooters-eletricas-na-cidade-vale-a-pena/">matéria sobre uso urbano</a> e volte ao vendedor com perguntas específicas.</p>
        """,
    },
    "review-naked-300.html": {
        "title": "Protocolo de avaliação de naked urbana | TV Duas Rodas",
        "description": "Protocolo TVDUASRODAS para documentar ergonomia, manobras, calor, consumo e custo de uma naked urbana de média cilindrada.",
        "h1": "Protocolo de avaliação para naked urbana de média cilindrada",
        "tag": "Protocolo editorial · Motos",
        "image": "/assets/img/uploads/naked-urbana-yamaha-mt03.webp",
        "image_alt": "Yamaha MT-03 exposta no Tokyo Motor Show de 2015",
        "image_caption": "Yamaha MT-03 usada como referência visual da categoria, não como unidade testada. Foto: PekePON / Wikimedia Commons, CC BY-SA 4.0.",
        "image_source": "https://commons.wikimedia.org/wiki/File:YAMAHA_MT-03_at_the_Tokyo_Motor_Show_2015.jpg",
        "bad_video": "xcPxjtQU1qc",
        "body": """
                  <p class="article-update-note"><strong>Atualizado em 22 ago 2026.</strong> Esta URL funciona como ficha de teste. A análise editorial está em <a href="/materias/naked-urbana-300cc-uso-real-na-cidade/">Naked urbana de 300 cc: uso real na cidade</a>.</p>

                  <p>Um review útil precisa separar impressão, medição e especificação do fabricante. Este protocolo mostra o que registrar para que dois trajetos ou duas motocicletas possam ser comparados sem transformar sensação isolada em dado universal.</p>

                  <h2>Antes de ligar a moto</h2>
                  <ul>
                    <li>Modelo, versão, ano, quilometragem e condição dos pneus;</li>
                    <li>combustível utilizado, acessórios instalados e carga transportada;</li>
                    <li>temperatura, chuva, vento e tipo de percurso;</li>
                    <li>pressão dos pneus e alertas presentes no painel.</li>
                  </ul>
                  <p>Confirme ficha técnica e intervalos de manutenção no manual do modelo exato. A foto ou a aparência não garantem que duas versões tenham os mesmos freios, suspensão ou eletrônica.</p>

                  <h2>Ergonomia parada</h2>
                  <p>Registre altura do piloto, alcance dos pés, ângulo de joelhos, apoio das mãos e esforço para retirar a moto do descanso. Faça manobras com motor desligado somente onde for seguro. Se houver passageiro, avalie banco, alças e pedaleiras sem ultrapassar a capacidade indicada pelo fabricante.</p>

                  <h2>Baixa velocidade e trânsito</h2>
                  <p>Em percurso autorizado, observe esterço, progressividade de acelerador e embreagem, facilidade de equilíbrio e calor percebido quando a ventoinha atua. Anote o tempo parado e a temperatura ambiente. Não conclua que toda unidade do modelo se comporta igual se a moto testada estiver com manutenção, pneus ou acessórios diferentes do padrão.</p>

                  <h2>Piso, suspensão e freios</h2>
                  <p>Descreva o pavimento e a velocidade aproximada ao avaliar conforto. Em via pública, não simule frenagem de emergência. Modulação, atuação de ABS e limites só devem ser explorados em ambiente fechado, com autorização e orientação qualificada. Para o uso diário, registre confiança nos comandos e estabilidade em situações normais.</p>

                  <h2>Consumo com método</h2>
                  <p>Use o mesmo procedimento em todas as motos: abastecimento no mesmo nível, hodômetro conferido, percurso descrito e bomba identificada. Mostre distância, volume e cálculo. Computador de bordo pode ser comparado ao método de abastecimento, mas não deve ser apresentado como medição independente sem essa ressalva.</p>

                  <h2>Custo de manter</h2>
                  <p>Peça cotações de seguro no CEP do interessado, preços de revisão, pneus, relação, pastilhas, manetes e peças expostas em uma queda leve. Some documentação e estacionamento. Uma motocicleta de compra mais barata pode ter seguro ou peças mais caros; o protocolo existe para tornar essa diferença visível.</p>

                  <h2>Como publicar a conclusão</h2>
                  <p>Liste primeiro os fatos medidos, depois as impressões do piloto e, por fim, para quais rotinas o conjunto parece adequado. Declare limitações do percurso. O <a href="/guias/review-naked-300/">guia aprofundado da categoria</a> complementa esta ficha sem substituir o manual nem um test ride próprio.</p>
        """,
    },
    "role-urbano-noturno.html": {
        "title": "Plano de rolê urbano noturno | TV Duas Rodas",
        "description": "Plano prático para preparar rota, iluminação, equipamento, formação do grupo e retorno seguro em um passeio urbano noturno.",
        "h1": "Plano de rolê urbano noturno: preparação, rota e briefing",
        "tag": "Planejamento · Segurança urbana",
        "image": "/assets/img/uploads/role-urbano-noturno-nyc.webp",
        "image_alt": "Motocicleta estacionada em rua urbana durante a noite",
        "image_caption": "Cena urbana noturna usada como ilustração, sem indicar uma rota. Foto: Jess Hawsor / Wikimedia Commons, CC BY-SA 4.0.",
        "image_source": "https://commons.wikimedia.org/wiki/File:NYC_-_motorcycle_parked_on_street_at_night.jpg",
        "bad_video": "kXYiU_JCYtU",
        "body": """
                  <p class="article-update-note"><strong>Atualizado em 22 ago 2026.</strong> Esta página é um roteiro operacional. Leia também a <a href="/materias/role-urbano-noturno-luzes-da-cidade-em-duas-rodas/">matéria de segurança para pilotagem noturna</a>.</p>

                  <p>O passeio começa antes da partida. Um plano curto reduz improvisos, evita que o grupo se disperse e deixa claro quando a saída deve ser adiada. Preencha os itens com locais reais e compartilhe o plano com todos os participantes.</p>

                  <h2>Condição de saída</h2>
                  <ul>
                    <li>Previsão de chuva, temperatura e visibilidade consultadas perto do horário;</li>
                    <li>farol baixo e alto, lanterna, luz de freio e setas funcionando;</li>
                    <li>viseira limpa e adequada ao período noturno;</li>
                    <li>pneus, combustível ou carga da bateria conferidos;</li>
                    <li>piloto descansado, alimentado e sem consumo de álcool.</li>
                  </ul>
                  <p>A <a href="https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-contran/resolucoes/Resolucao9402022.pdf" target="_blank" rel="noopener">Resolução Contran nº 940/2022</a> determina viseira cristal à noite. Equipamento regular não elimina a necessidade de reduzir o ritmo quando chuva, neblina ou iluminação ruim encurtarem a visão.</p>

                  <h2>Ficha da rota</h2>
                  <p>Registre ponto de encontro, horário limite de saída, destino, distância, posto ou recarga, parada intermediária e local de encerramento. Escolha vias conhecidas e pontos de apoio abertos. Tenha uma alternativa para obra, alagamento, bloqueio ou mudança de clima. Compartilhe a rota com uma pessoa que não participa do passeio.</p>

                  <h2>Briefing de cinco minutos</h2>
                  <ul>
                    <li>Cada piloto respeita semáforos e confirma individualmente o cruzamento;</li>
                    <li>ninguém acelera para alcançar o grupo;</li>
                    <li>a formação mantém distância e não ocupa pontos cegos;</li>
                    <li>um integrante conhece o caminho e outro fecha o grupo;</li>
                    <li>em caso de separação, todos seguem para a próxima parada combinada.</li>
                  </ul>

                  <h2>Comunicação sem distração</h2>
                  <p>Configure navegação e intercomunicador antes de partir. Não manuseie telefone em movimento. Defina sinais simples para parada, combustível e problema mecânico, mas não dependa deles como substitutos das regras de trânsito.</p>

                  <h2>Critérios para encerrar</h2>
                  <p>Chuva forte, falha de iluminação, pneu com perda de pressão, sonolência ou integrante desconfortável são motivos suficientes para parar. Escolha local iluminado e fora do fluxo. Se não houver condição de retorno, use transporte alternativo e recupere a moto depois.</p>

                  <h2>Registro pós-rolê</h2>
                  <p>Anote trechos escuros, obras, pontos de apoio fechados e tempo real do percurso. Essa informação melhora o próximo plano. O <a href="/guias/role-urbano-noturno/">guia editorial completo</a> reúne contexto adicional; esta página permanece como checklist reutilizável.</p>
        """,
    },
    "viagem-serra-mirantes.html": {
        "title": "Planejador de viagem de serra | TV Duas Rodas",
        "description": "Planejador editorial para rota de serra com clima, combustível, descidas, paradas, equipamento e contatos de apoio.",
        "h1": "Planejador de viagem de serra: rota, clima e margens",
        "tag": "Planejamento de viagem · Estrada",
        "image": "/assets/img/uploads/estrada-graciosa-curvas-commons.webp",
        "image_alt": "Curvas fechadas na Estrada da Graciosa, no Paraná",
        "image_caption": "Curvas fechadas da Estrada da Graciosa, usadas como exemplo visual de rota de serra. Foto: Rodrigo Postol / Wikimedia Commons, CC BY-SA 4.0.",
        "image_source": "https://commons.wikimedia.org/wiki/File:Estrada_da_Graciosa_4.jpg",
        "bad_video": "hTWKbfoikeg",
        "body": """
                  <p class="article-update-note"><strong>Atualizado em 22 ago 2026.</strong> Esta página é uma ficha de planejamento. A leitura narrativa está em <a href="/materias/viagem-de-serra-mirantes-curvas-e-seguranca/">Viagem de serra: mirantes, curvas e segurança</a>.</p>

                  <p>Serra reúne variação de clima, curvas, desnível, neblina e tráfego turístico em um mesmo trajeto. O objetivo deste plano não é prometer uma rota sem risco, mas tornar visíveis as decisões que precisam ser tomadas antes e durante a viagem.</p>

                  <h2>Defina limites, não apenas o destino</h2>
                  <ul>
                    <li>Distância total e maior intervalo entre combustível ou recarga;</li>
                    <li>horário máximo para iniciar a subida e a descida;</li>
                    <li>ponto de retorno caso o clima feche;</li>
                    <li>paradas seguras e mirantes com acesso permitido;</li>
                    <li>hospedagem ou transporte alternativo se a etapa não puder continuar.</li>
                  </ul>

                  <h2>Cheque fontes perto da partida</h2>
                  <p>Consulte previsão meteorológica, avisos da concessionária ou órgão rodoviário e canais municipais. Confirme bloqueios, obras e horário de atrações diretamente com a fonte responsável. Uma postagem antiga não comprova que o acesso continua aberto. Guarde os links e o horário da consulta.</p>

                  <h2>Prepare a motocicleta</h2>
                  <p>Verifique pneus, freios, iluminação, transmissão, fluidos e fixação da bagagem conforme o manual. Faça manutenção com antecedência suficiente para testar a moto antes da viagem. Distribua carga sem superar limites do fabricante e mantenha itens de chuva acessíveis.</p>

                  <h2>Planeje a descida</h2>
                  <p>Descidas longas exigem velocidade compatível, marcha adequada e espaço. Não dependa de frenagem contínua como única forma de controle. Se houver mudança de resposta nos freios, odor anormal ou alerta no painel, pare em local seguro e procure assistência. Técnica específica deve ser treinada com profissional, não improvisada durante a viagem.</p>

                  <h2>Curva, neblina e tráfego local</h2>
                  <p>Entre em cada curva com margem para o que ainda não está visível. Neblina, animais, ciclistas, ônibus e veículos parados podem ocupar a trajetória. Respeite faixa, limite e sinalização; não use a estrada como pista e não pare no acostamento para fotografar quando houver mirante ou área autorizada.</p>

                  <h2>Ficha de apoio</h2>
                  <ul>
                    <li>Contato de emergência e pessoa que recebeu o roteiro;</li>
                    <li>seguradora ou assistência, oficinas e hospitais do trajeto;</li>
                    <li>documentos, meios de pagamento e telefone protegido da chuva;</li>
                    <li>água, camada térmica e medicamento de uso pessoal;</li>
                    <li>localização das paradas salva para uso sem sinal.</li>
                  </ul>

                  <h2>Revisão no dia</h2>
                  <p>Compare o plano com o clima, a condição física e a moto naquele momento. Adiar não é falhar; é aplicar o limite definido. Consulte o <a href="/guias/viagem-serra-mirantes/">guia editorial aprofundado</a> para contexto adicional e atualize esta ficha a cada novo percurso.</p>
        """,
    },
}


def replace_once(text: str, pattern: str, replacement: str, path: Path) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f"Trecho esperado não encontrado uma vez em {path}: {pattern[:60]}")
    return updated


def main() -> int:
    for filename, data in HUBS.items():
        path = ROOT / filename
        text = path.read_text(encoding="utf-8-sig")
        text = replace_once(text, r"<title>.*?</title>", f"<title>{data['title']}</title>", path)
        text = replace_once(
            text,
            r'<meta name="description" content="[^"]*"\s*/>',
            f'<meta name="description" content="{data["description"]}" />',
            path,
        )
        text = replace_once(text, r"<h1>.*?</h1>", f"<h1>{data['h1']}</h1>", path)
        text = replace_once(
            text,
            r'<span class="category-tag">.*?</span>',
            f'<span class="category-tag">{data["tag"]}</span>',
            path,
        )
        text = text.replace(
            '<a href="#" class="social-icon">YT</a>',
            '<a href="https://www.youtube.com/@tvduasrodas?sub_confirmation=1" class="social-icon" '
            'aria-label="TVDUASRODAS no YouTube">YT</a>',
        )
        text = text.replace(
            '<a href="#" class="social-icon">IG</a>',
            '<a href="https://www.instagram.com/tvduasrodasofc" class="social-icon" '
            'aria-label="TVDUASRODAS no Instagram">IG</a>',
        )
        text = text.replace('<a href="#" class="social-icon">TT</a>', "")
        hero = (
            '<section class="article-hero">\n'
            '                  <figure class="article-hero-media">\n'
            f'                    <img src="{data["image"]}" alt="{data["image_alt"]}" '
            'loading="eager" decoding="async">\n'
            f'                    <figcaption>{data["image_caption"]} '
            f'<a href="{data["image_source"]}" target="_blank" rel="noopener noreferrer">Fonte da imagem</a>.</figcaption>\n'
            '                  </figure>\n'
            '              </section>'
        )
        text = replace_once(
            text,
            r'<section class="article-hero">.*?</section>',
            hero,
            path,
        )
        text = re.sub(
            rf'\s*<li><a href="tv\.html\?v={re.escape(data["bad_video"])}">.*?</a></li>',
            "",
            text,
            count=1,
            flags=re.DOTALL,
        )
        text = replace_once(
            text,
            r'(?:<!-- CORPO (?:DA MATÉRIA|EDITORIAL PRÓPRIO) -->\s*)?<section class="article-body">.*?</section>',
            '<!-- CORPO EDITORIAL PRÓPRIO -->\n              <section class="article-body">\n'
            + data["body"].strip("\n")
            + '\n              </section>',
            path,
        )
        text = re.sub(
            r'\s*<!-- BARRA TOPO \(ANÚNCIO\) -->\s*<div class="ad-bar">.*?</div>\s*</div>',
            "",
            text,
            count=1,
            flags=re.DOTALL,
        )
        text = re.sub(
            r'\s*(?:<!-- PATROCÍNIO NO TOPO DA MATÉRIA -->\s*)?<div class="article-sponsor">.*?</div>',
            "",
            text,
            count=1,
            flags=re.DOTALL,
        )
        text = re.sub(
            r'\s*<div class="ad-slot ad-slot-sidebar">.*?</div>',
            "",
            text,
            count=1,
            flags=re.DOTALL,
        )
        text = re.sub(
            r'\s*<div class="footer-ad">\s*<div class="ad-slot ad-slot-small">.*?</div>\s*</div>',
            "",
            text,
            count=1,
            flags=re.DOTALL,
        )
        if 'href="/politica-editorial"' not in text:
            footer_intro = (
                '<p class="footer-small">TV &amp; Revista eletrônica para apaixonados por duas rodas.</p>'
            )
            trust_links = (
                '<p class="footer-small"><a href="/sobre">Sobre</a> · <a href="/equipe">Equipe</a> · '
                '<a href="/contato">Contato</a> · <a href="/politica-editorial">Política editorial</a> · '
                '<a href="/politica-de-correcoes">Correções</a> · '
                '<a href="/politica-de-privacidade">Privacidade</a> · <a href="/termos">Termos</a> · '
                '<a href="/sitemap.xml">Sitemap</a></p>'
            )
            text = replace_once(text, re.escape(footer_intro), footer_intro + "\n        " + trust_links, path)
        if re.search(r"EcoRide|Patrocínio:|Patrocinador topo|Patrocinador lateral|Patrocinador rodapé", text, re.I):
            raise ValueError(f"Placeholder publicitário permaneceu em {path}")
        if data["bad_video"] in text:
            raise ValueError(f"Vídeo-placeholder permaneceu em {path}")
        text = "\n".join(line.rstrip() for line in text.splitlines()).rstrip() + "\n"
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"Atualizado: {filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
