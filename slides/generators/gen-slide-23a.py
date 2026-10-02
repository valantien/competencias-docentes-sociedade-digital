# -*- coding: utf-8 -*-
"""Slide 23a — destaque 54% + tendencia 2021-2024 por dependencia administrativa.
Posicoes e desempilhamento de rotulos calculados aqui (regra do AGENTS.md)."""
import io, os, textwrap

DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "25-54-formacao-continuada.html")

YEARS = [2021, 2022, 2024]          # espacamento real: 2022->2024 e o dobro de 2021->2022
SERIES = [                          # cores fixas por entidade (mesmas dos slides 17 e 22)
    ("Total",      "#E9A36B",    [65, 56, 54]),   # pêssego grosso, como o Total da tela 25 (sem preto — pedido do usuário, 2026-09-12)
    ("Municipal",  "var(--o1)",  [62, 50, 43]),
    ("Estadual",   "var(--o2)",  [69, 63, 62]),
    ("Particular", "var(--o3)",  [66, 50, 58]),
]

W, H = 728, 520            # ocupa a altura do corpo (534px) — esticado em 2026-09-12
X0, X1 = 58, 494
Y0, VMAX, YTOP = 470, 80, 30
def x(year): return X0 + (year - YEARS[0]) / (YEARS[-1] - YEARS[0]) * (X1 - X0)
def y(v):    return Y0 - v * (Y0 - YTOP) / VMAX

def declutter(items, gap):
    items = sorted(items, key=lambda t: t[0])
    out = []
    for yy, h, p in items:
        if out:
            lo = out[-1][0] + out[-1][1] / 2 + gap + h / 2
            if yy < lo: yy = lo
        out.append([yy, h, p])
    over = out[-1][0] + out[-1][1] / 2 - (Y0 + 6)
    if over > 0:
        for it in out: it[0] -= over
    return out

s = []
A = s.append
for v in range(0, VMAX + 1, 20):
    A(f'<line class="grid" x1="{X0-26}" x2="{X1+8}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>')
    A(f'<text class="ax" x="{X0-34}" y="{y(v)+4:.1f}" text-anchor="end">{v}</text>')
A(f'<line class="axis" x1="{X0-26}" x2="{X1+8}" y1="{y(0):.1f}" y2="{y(0):.1f}"/>')

for name, color, vals in SERIES:
    P = [f"{x(yr):.1f},{y(v):.1f}" for yr, v in zip(YEARS, vals)]
    # 2021->2022: dado anual (contínua). 2022->2024: sem observação em 2023 (tracejada, com legenda) — regra do AGENTS.md
    larg = "stroke-width:7;" if name == "Total" else ""   # style, não atributo: o CSS .ln venceria o atributo
    pont = "0.1 13" if name == "Total" else "2 9"
    A(f'<polyline class="ln" points="{P[0]} {P[1]}" stroke="{color}" style="{larg}"/>')
    A(f'<polyline class="ln" points="{P[1]} {P[2]}" stroke="{color}" style="{larg}stroke-dasharray:{pont}"/>')
for name, color, vals in SERIES:
    for yr, v in zip(YEARS, vals):
        A(f'<circle class="mk" cx="{x(yr):.1f}" cy="{y(v):.1f}" r="5.5" stroke="{color}"/>')

# rotulos de valor so nos extremos (regra da skill dataviz: rotulo direto seletivo,
# nunca um numero em cada ponto). 2022 se le pela forma da linha e pela grade.
uniq = sorted({vals[0] for _n, _c, vals in SERIES})
for yy, _h, v in declutter([(y(v), 15, v) for v in uniq], 4):
    A(f'<text class="val" x="{x(YEARS[0])-12:.1f}" y="{yy+4:.1f}" text-anchor="end">{v}</text>')

# 2024: nome + valor a direita (rotulo direto = legenda, identidade nunca so pela cor)
blocks = [(y(vals[-1]), 18, (name, color, vals[-1])) for name, color, vals in SERIES]
for yy, _h, (name, color, v) in declutter(blocks, 6):
    A(f'<circle cx="{X1+26}" cy="{yy:.1f}" r="5" fill="{color}"/>')
    A(f'<text class="nm" x="{X1+38}" y="{yy+4:.1f}">{name}</text>')
    A(f'<text class="nmv" x="{W-8}" y="{yy+4:.1f}" text-anchor="end">{v}</text>')

# legenda da convenção de linha (contínua = dado anual; pontilhada = intervalo sem dado)
A(f'<line x1="{X1+26}" x2="{X1+66}" y1="300" y2="300" stroke="#8F3B15" stroke-width="3" stroke-linecap="round"/>')
A(f'<text class="nm" x="{X1+74}" y="305" style="font-weight:400">dado anual</text>')
A(f'<line x1="{X1+26}" x2="{X1+66}" y1="326" y2="326" stroke="#8F3B15" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 9"/>')
A(f'<text class="nm" x="{X1+74}" y="331" style="font-weight:400">sem dado em 2023</text>')

for yr in YEARS:
    A(f'<text class="yr" x="{x(yr):.1f}" y="{Y0+27}" text-anchor="middle">{yr}</text>')

svg = "\n        ".join(s)

HTML = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Slide 23a — Formação continuada, tendência</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
<style>
  :root{{
    --ink:#1E1B18; --paper:#EFE3D1; --orange:#C1541F; --orange-deep:#8F3B15;
    --orange-soft:#E8792F; --peach:#F3C7A4; --grid:#DCD1BF; --muted:#8A7F73;
    --o1:#C0501A; --o2:#1F5FA8; --o3:#0E7F63;
    --sans:"Roboto Condensed",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    --serif:"Fraunces",Georgia,serif;
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{height:100%;background:#241B14}}
  body{{display:flex;align-items:center;justify-content:center;font-family:var(--sans)}}
  .stage{{position:relative;width:1280px;height:720px;background:var(--paper);
    overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.45);border-radius:6px;
    padding:36px 56px 30px;display:flex;flex-direction:column}}
  .s-head{{margin-bottom:8px}}
  .eyebrow{{font-size:.8rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;
    color:var(--orange-soft);margin-bottom:6px;display:flex;align-items:center;gap:12px}}
  .eyebrow::before{{content:"";width:24px;height:2px;background:var(--orange-soft);display:inline-block}}
  /* título em UMA linha (pedido do usuário, 2026-09-12): a nota do universo desce para baixo dele */
  .head-row{{display:flex;flex-direction:column;align-items:flex-start;gap:4px}}
  .s-title{{font-size:1.26rem;line-height:1.24;font-weight:700;color:var(--orange-deep);flex:1}}
  .s-note{{flex:none;font-size:.8rem;line-height:1.35;color:var(--muted);
    padding-left:0;border-left:none}}
  .accent-rule{{height:3px;width:100%;margin-top:10px;border-radius:2px;
    background:linear-gradient(90deg,var(--orange-deep) 0%,var(--orange) 45%,var(--peach) 100%)}}

  .body{{flex:1;display:flex;align-items:center;gap:40px;min-height:0;padding-top:6px}}
  .stat{{flex:0 0 400px}}
  .stat-num{{font-family:var(--serif);font-weight:600;font-size:7.4rem;line-height:.86;
    color:var(--orange-deep);letter-spacing:-.03em}}
  .stat-num span{{font-size:3.1rem;letter-spacing:0}}
  .stat-txt{{font-size:1.16rem;line-height:1.4;font-weight:600;color:var(--ink);margin-top:16px}}
  .stat-txt b{{color:var(--orange-deep)}}
  .stat-note{{margin-top:22px;padding:14px 16px;border-left:3px solid var(--orange);
    background:#FDF2E9;font-size:.9rem;line-height:1.45;color:var(--ink)}}
  .stat-note .kicker{{display:block;font-size:.8rem;font-weight:700;letter-spacing:.14em;
    text-transform:uppercase;color:var(--orange);margin-bottom:6px}}
  .stat-note b{{color:var(--orange-deep)}}

  .chart{{flex:1;display:flex;justify-content:center;min-width:0}}
  svg{{width:{W}px;height:{H}px;display:block}}
  .grid{{stroke:var(--grid);stroke-width:1}}
  .axis{{stroke:#B3A894;stroke-width:1.5}}
  .ln{{fill:none;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}}
  .mk{{fill:var(--paper);stroke-width:2.5}}
  .val{{font-size:15px;font-weight:700;fill:var(--ink)}}
  .ax{{font-size:15px;fill:var(--muted)}}
  .yr{{font-size:15px;font-weight:700;fill:var(--ink)}}
  .nm{{font-size:15px;font-weight:600;fill:var(--ink)}}
  .nmv{{font-size:15px;font-weight:800;fill:var(--ink)}}

  .m-src{{margin-top:8px;padding-top:8px;border-top:1px solid var(--muted);
    font-size:.72rem;color:var(--muted);font-style:italic;line-height:1.35}}
  .m-src a{{color:inherit}}
</style>
</head>
<body>

<div class="stage">
  <div class="s-head">
    <div class="eyebrow">Professores</div>
    <div class="head-row">
      <h1 class="s-title">Professores que participaram de formação continuada sobre tecnologias digitais nos 12 meses anteriores à realização da pesquisa</h1>
      <div class="s-note">Total de professores de escolas de Ensino Fundamental e Médio (%)</div>
    </div>
    <div class="accent-rule"></div>
  </div>

  <div class="body">
    <div class="stat">
      <div class="stat-num">54<span>%</span></div>
      <div class="stat-txt">dos professores participaram de formação continuada sobre <b>tecnologias digitais</b> nos processos de ensino e de aprendizagem</div>
      <div class="stat-note">
        <span class="kicker">A tendência</span>
        Eram <b>65%</b> em 2021. A queda atinge todas as redes, mas é <b>muito mais forte na rede municipal</b>: de 62% para 43% — 19 pontos em três anos.
      </div>
    </div>
    <div class="chart">
      <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img"
           aria-label="Participação em formação continuada sobre tecnologias digitais, de 2021 a 2024, por dependência administrativa.">
        {svg}
      </svg>
    </div>
  </div>

  <div class="m-src">Fonte: Cetic.br/NIC.br, Pesquisa TIC Educação 2021, 2022 e 2024. <a href="https://cetic.br/pt/pesquisa/educacao/">https://cetic.br/pt/pesquisa/educacao/</a></div>
</div>

</body>
</html>
'''
io.open(DST, "w", encoding="utf-8").write(HTML)
print("gerado:", os.path.normpath(DST))
