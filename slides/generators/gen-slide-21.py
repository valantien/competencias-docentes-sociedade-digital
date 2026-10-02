# -*- coding: utf-8 -*-
"""Gera o SVG do slope chart do slide 21 com posicoes calculadas."""
import io, textwrap, os

SERIES = [
    ("Uso excessivo de jogos digitais e tecnologias", "#C0501A", [(43,46),(50,58),(42,58)]),
    ("Cyberbullying",                                  "#1F5FA8", [(27,29),(40,39),(30,38)]),
    ("Discriminação",                                  "#0E7F63", [(22,28),(34,38),(30,32)]),
    ("Disseminação ou vazamento de imagens sem consentimento", "#96700A", [(20,14),(28,28),(29,21)]),
    ("Assédio",                                        "#B23A6B", [(17,17),(19,26),(23,11)]),
    ("Outras situações ocorridas na Internet",         "#1F6B1F", [(3,3),(5,6),(8,6)]),
]
PANELS = ["Anos iniciais do Ensino Fundamental (4º e 5º ano)",
          "Anos finais do Ensino Fundamental",
          "Ensino Médio"]

W, H = 1160, 530          # altura cheia do chart-col (535px) — esticado em 2026-09-12
OFFS = [0, 310, 620]
PW = 300                      # largura util de cada painel
Y0, VMAX, YMAX = 440, 60, 30  # y do valor 0, valor maximo, y do valor maximo
def y(v): return Y0 - v * (Y0 - YMAX) / VMAX

def declutter(items, gap):
    """items: [(y_desejado, altura, payload)] -> mesma lista com y sem sobreposicao."""
    items = sorted(items, key=lambda t: t[0])
    placed = []
    for yy, h, p in items:
        if placed:
            miny = placed[-1][0] + placed[-1][1] / 2 + gap + h / 2
            if yy < miny: yy = miny
        placed.append([yy, h, p])
    # empurra para cima se estourou o limite inferior
    over = placed[-1][0] + placed[-1][1] / 2 - (Y0 + 8)
    if over > 0:
        for it in placed: it[0] -= over
    return placed

def wrap(txt, n):
    return textwrap.wrap(txt, n) or [txt]

out = []
A = out.append

# --- grade + eixo ---
for v in range(0, VMAX + 1, 10):
    A(f'<line class="grid" x1="8" x2="912" y1="{y(v):.1f}" y2="{y(v):.1f}"/>')
A(f'<line class="axis" x1="8" x2="912" y1="{y(0):.1f}" y2="{y(0):.1f}"/>')
for x in (305, 615):
    A(f'<line class="sep" x1="{x}" x2="{x}" y1="{YMAX-4}" y2="{Y0+56}"/>')

# --- linhas, marcadores, rotulos de valor ---
for pi, off in enumerate(OFFS):
    xa, xb = off + 48, off + 248
    for name, color, vals in SERIES:
        a, b = vals[pi]
        A(f'<line class="ln" x1="{xa}" x2="{xb}" y1="{y(a):.1f}" y2="{y(b):.1f}" stroke="{color}"/>')
    for name, color, vals in SERIES:
        a, b = vals[pi]
        A(f'<circle class="dot" cx="{xa}" cy="{y(a):.1f}" r="5" stroke="{color}"/>')
        A(f'<circle class="dot" cx="{xb}" cy="{y(b):.1f}" r="5" stroke="{color}"/>')
    # rotulos de valor, com desempilhamento por lado
    for side, xi, anchor, idx in (("L", off + 38, "end", 0), ("R", off + 258, "start", 1)):
        seen = {}
        for name, color, vals in SERIES:
            v = vals[pi][idx]
            seen.setdefault(v, True)          # valores iguais compartilham 1 rotulo
        blocks = declutter([(y(v), 15, v) for v in seen], 3)
        for yy, _h, v in blocks:
            A(f'<text class="val" x="{xi}" y="{yy+4:.1f}" text-anchor="{anchor}">{v}</text>')
    # anos + etapa
    A(f'<text class="yr" x="{xa}" y="{Y0+28}" text-anchor="middle">2022</text>')
    A(f'<text class="yr" x="{xb}" y="{Y0+28}" text-anchor="middle">2024</text>')
    lines = wrap(PANELS[pi], 34)
    for li, ln in enumerate(lines):
        A(f'<text class="pnl" x="{off+148}" y="{Y0+52+li*18}" text-anchor="middle">{ln}</text>')

# --- coluna de nomes: legenda e rotulo direto ao mesmo tempo ---
NX = 930
blocks = []
for name, color, vals in SERIES:
    ls = wrap(name, 26)
    blocks.append((y(vals[2][1]), len(ls) * 19, (name, color, ls)))
for yy, h, (name, color, ls) in declutter(blocks, 11):
    top = yy - h / 2 + 11
    A(f'<circle cx="{NX+5}" cy="{yy:.1f}" r="5" fill="{color}"/>')
    for li, ln in enumerate(ls):
        x = NX + 18
        A(f'<text class="nm" x="{x}" y="{top+li*19:.1f}">{ln}</text>')

svg = "\n      ".join(out)

HTML = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Slide 21 — Professores que apoiaram alunos em situações sensíveis</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
<style>
  :root{{
    --ink:#1E1B18; --paper:#EFE3D1; --orange:#C1541F; --orange-deep:#8F3B15;
    --orange-soft:#E8792F; --peach:#F3C7A4; --grid:#DCD1BF; --muted:#8A7F73;
    --sans:"Roboto Condensed",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{height:100%;background:#241B14}}
  body{{display:flex;align-items:center;justify-content:center;font-family:var(--sans)}}
  .stage{{
    position:relative;width:1280px;height:720px;background:var(--paper);
    overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.45);border-radius:6px;
    padding:36px 60px 30px;display:flex;flex-direction:column;
  }}
  .s-head{{margin-bottom:8px}}
  .eyebrow{{
    font-size:.8rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;
    color:var(--orange-soft);margin-bottom:6px;display:flex;align-items:center;gap:12px;
  }}
  .eyebrow::before{{content:"";width:24px;height:2px;background:var(--orange-soft);display:inline-block}}
  /* título em UMA linha (pedido do usuário, 2026-09-12): a nota do universo desce para baixo dele */
  .head-row{{display:flex;flex-direction:column;align-items:flex-start;gap:4px}}
  .s-title{{font-size:1.2rem;line-height:1.24;font-weight:700;color:var(--orange-deep);flex:1}}
  .s-note{{flex:none;font-size:.8rem;line-height:1.35;color:var(--muted);
    padding-left:0;border-left:none}}
  .accent-rule{{height:3px;width:100%;margin-top:10px;border-radius:2px;
    background:linear-gradient(90deg,var(--orange-deep) 0%,var(--orange) 45%,var(--peach) 100%)}}

  .chart-col{{flex:1;display:flex;flex-direction:column;justify-content:center;min-height:0;padding-top:8px}}
  svg{{width:{W}px;height:{H}px;display:block}}
  .grid{{stroke:var(--grid);stroke-width:1}}
  .axis{{stroke:#B3A894;stroke-width:1.5}}
  .sep{{stroke:var(--grid);stroke-width:1}}
  .ln{{stroke-width:2.5;stroke-linecap:round}}
  .dot{{fill:var(--paper);stroke-width:2.5}}
  .val{{font-size:15px;font-weight:700;fill:var(--ink)}}
  .yr{{font-size:15px;font-weight:700;fill:var(--ink)}}
  .pnl{{font-size:14px;fill:var(--muted)}}
  .nm{{font-size:15px;font-weight:600;fill:var(--ink)}}

  .m-src{{margin-top:10px;padding-top:8px;border-top:1px solid var(--muted);
    font-size:.72rem;color:var(--muted);font-style:italic;line-height:1.35}}
  .m-src a{{color:inherit}}
</style>
</head>
<body>

<div class="stage">
  <div class="s-head">
    <div class="eyebrow">Professores</div>
    <div class="head-row">
      <h1 class="s-title">Professores que apoiaram alunos no enfrentamento de situações sensíveis ocorridas na Internet, nos 12 meses anteriores à realização da pesquisa</h1>
      <div class="s-note">Total de professores de escolas de Ensino Fundamental e Médio (%)</div>
    </div>
    <div class="accent-rule"></div>
  </div>

  <div class="chart-col">
    <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img"
         aria-label="Gráfico de inclinação: seis situações sensíveis comparadas entre 2022 e 2024, em três etapas de ensino.">
      {svg}
    </svg>
  </div>

  <div class="m-src">Fonte: Cetic.br/NIC.br, Pesquisa TIC Educação 2022 e 2024. <a href="https://cetic.br/pt/pesquisa/educacao/">https://cetic.br/pt/pesquisa/educacao/</a></div>
</div>

</body>
</html>
'''
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fora-21-professores-apoio-situacoes-sensiveis.html")
io.open(p, "w", encoding="utf-8").write(HTML)
print("gerado:", p)
