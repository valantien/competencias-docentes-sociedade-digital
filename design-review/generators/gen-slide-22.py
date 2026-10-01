# -*- coding: utf-8 -*-
"""Slide 22 — clona a estrutura aprovada do slide 19 e calcula os deslocamentos
de nos coincidentes automaticamente (regra do AGENTS.md)."""
import io, re, os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fora-19-alunos-recursos-pesquisa.html")
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fora-22-escolas-convivencia-participativa.html")

# (rotulo HTML, total, municipal, estadual, particular)
ROWS = [
 ("Plano de <b>convivência escolar</b> integrado ao Projeto Político-Pedagógico", 82, 78, 87, 90),
 ("<b>Canal de comunicação e escuta</b> aberto entre alunos, professores, funcionários e famílias", 81, 79, 84, 83),
 ("<b>Plano individualizado de acompanhamento</b> de alunos que necessitam de maior atenção em relação a vulnerabilidades ou comportamentos reincidentes", 79, 76, 81, 86),
 ("<b>Rede de apoio permanente</b>, formada por adultos de referência a quem os alunos possam buscar auxílio caso vivenciem situações sensíveis", 73, 68, 82, 76),
 ("<b>Grupo permanente de mediação de conflitos</b>", 64, 62, 72, 62),
 ("<b>Sistema de apoio estudantil</b>, no qual os próprios alunos ajudam uns aos outros a lidar com situações sensíveis", 61, 58, 65, 63),
]

LABEL_W, TABLE_W, INNER = 318, 196, 1168
TRACK_PX = INNER - LABEL_W - TABLE_W
DOT_PX = 14
THRESH = DOT_PX / (TRACK_PX / 100.0) * 1.2      # em unidades de valor, com folga

def nudges(vals):
    """vals: [(classe, valor)] -> {classe: ''|' nudge-up'|' nudge-dn'}"""
    out = {c: "" for c, _ in vals}
    order = sorted(vals, key=lambda t: t[1])
    cluster = [order[0]]
    for cur in order[1:]:
        if cur[1] - cluster[-1][1] <= THRESH:
            cluster.append(cur)
        else:
            _apply(cluster, out); cluster = [cur]
    _apply(cluster, out)
    return out

def _apply(cluster, out):
    """Desloca so para baixo: acima da linha fica o rotulo do total."""
    for k, (cls, _v) in enumerate(cluster[1:], start=1):
        out[cls] = " nudge-dn" if k == 1 else " nudge-dn2"

COLOR = {"d1":"var(--o1)", "d2":"var(--o2)", "d3":"var(--o3)"}

PX_UNIT = TRACK_PX / 100.0
MIN_SEP = 16.0          # distancia minima entre centros de nos (px)

def dots_html(mun, est, par):
    """Todos os nos na mesma horizontal. Quando dois ficariam sobrepostos,
    afasta lateralmente o minimo necessario (licenca poetica) via margin-left,
    mantendo `left` no valor real. A leitura exata fica na tabela a direita."""
    vals = sorted([("d1", mun), ("d2", est), ("d3", par)], key=lambda t: t[1])
    clusters, cur = [], [vals[0]]
    for c, v in vals[1:]:
        if (v - cur[-1][1]) * PX_UNIT < MIN_SEP:
            cur.append((c, v))
        else:
            clusters.append(cur); cur = [(c, v)]
    clusters.append(cur)

    out = []
    for cl in clusters:
        if len(cl) == 1:
            c, v = cl[0]
            out.append(f'<div class="dot {c}" style="left:{v}%"></div>')
            continue
        n = len(cl)
        mean_px = sum(v for _c, v in cl) / n * PX_UNIT
        for i, (c, v) in enumerate(cl):
            target = mean_px + (i - (n - 1) / 2) * MIN_SEP
            margin = target - v * PX_UNIT
            out.append(f'<div class="dot {c}" style="left:{v}%;margin-left:{margin:.1f}px"></div>')
    return "".join(out)

rows_html = []
for lab, tot, mun, est, par in ROWS:
    rows_html.append(f'''    <div class="row">
      <div class="row-label">{lab}</div>
      <div class="track"><div class="base-line"></div>
        <div class="total-line" style="width:{tot}%"></div><div class="total-val" style="left:{tot}%">{tot}</div>
        {dots_html(mun, est, par)}
      </div>
      <div class="tbl"><span>{mun}</span><span>{est}</span><span>{par}</span></div>
    </div>''')

s = io.open(SRC, encoding="utf-8").read()

# --- ajustes de estilo: coluna de rotulo mais larga, linhas mais altas (6 em vez de 10) ---
# Toda troca aqui é OBRIGATÓRIA: se o slide 19 mudar e o trecho sumir, o script para
# (antes falhava em silêncio e desalinhava eixo e linhas — ver MISTAKES.md).
def troca(s, a, b):
    assert s.count(a) == 1, f"trecho do slide 19 não encontrado (o template mudou?):\n  {a}"
    return s.replace(a, b)
s = troca(s, ".axis-top{display:grid;grid-template-columns:290px 1fr 150px;",
             f".axis-top{{display:grid;grid-template-columns:{LABEL_W}px 1fr {TABLE_W}px;")
s = troca(s, "  .row{display:grid;grid-template-columns:290px 1fr 150px;align-items:center;gap:0;",
             f"  .row{{display:grid;grid-template-columns:{LABEL_W}px 1fr {TABLE_W}px;align-items:center;gap:0;")
# folga entre o eixo e a 1ª linha (o rótulo do total da 1ª linha encostava nos números do eixo)
s = troca(s, "margin-bottom:2px;padding:0 10px 0 14px}", "margin-bottom:16px;padding:0 10px 0 14px}")
# cabeçalho da tabela sem caixa alta: "Municipal Estadual Particular" cabe nos 196px sem espremer
s = troca(s, "    text-transform:uppercase;letter-spacing:.03em;justify-content:space-around;text-align:center}",
             "    text-transform:none;letter-spacing:0;justify-content:space-around;text-align:center;padding-left:12px}")
# nos coincidentes descem; a faixa acima da linha fica livre para o rotulo do total

# --- cabecalho ---
s = s.replace("<title>Slide 19 — Alunos, recursos digitais em pesquisas escolares</title>",
              "<title>Slide 22 — Escolas, convivência participativa</title>")
s = s.replace('<div class="eyebrow">Alunos e recursos digitais</div>',
              '<div class="eyebrow">Escolas e convivência</div>')
s = re.sub(r'<h1 class="s-title">.*?</h1>',
           '<h1 class="s-title">Escolas, presença de espaços de apoio e promoção de convivência participativa para os alunos</h1>',
           s, count=1, flags=re.S)
s = s.replace('<div class="tbl-head"><span>Anos iniciais</span><span>Anos finais</span><span>Ens. Médio</span></div>',
              '<div class="tbl-head"><span>Municipal</span><span>Estadual</span><span>Particular</span></div>')

# --- corpo: troca todas as linhas ---
s = re.sub(r'(<div class="rows">\n).*?(\n  </div>\n\n  <div class="legend">)',
           lambda m: m.group(1) + "\n\n".join(rows_html) + m.group(2), s, count=1, flags=re.S)

# --- legenda ---
s = s.replace('style="background:var(--o1)"></span>Anos iniciais do Ensino Fundamental',
              'style="background:var(--o1)"></span>Municipal')
s = s.replace('style="background:var(--o2)"></span>Anos finais do Ensino Fundamental',
              'style="background:var(--o2)"></span>Estadual')
s = s.replace('style="background:var(--o3)"></span>Ensino Médio',
              'style="background:var(--o3)"></span>Particular')

# --- fonte ---
s = re.sub(r'<div class="m-src">.*?</div>',
  '<div class="m-src">Fonte: Cetic.br/NIC.br, Pesquisa TIC Educação 2021 — total de escolas (%). <a href="https://cetic.br/pt/pesquisa/educacao/">https://cetic.br/pt/pesquisa/educacao/</a></div>',
  s, count=1, flags=re.S)

io.open(DST, "w", encoding="utf-8").write(s)
print("gerado. limiar de sobreposicao:", round(THRESH,2), "unidades")
for lab, tot, mun, est, par in ROWS:
    h = dots_html(mun, est, par)
    if "margin-left" in h:
        moved = re.findall(r"left:(\\d+)%;margin-left:(-?[\\d.]+)px", h)
        print("  afastado:", lab[:42].replace("<b>", "").replace("</b>", ""),
              "->", ", ".join(f"{v}% {float(m):+.1f}px" for v, m in moved))
