# -*- coding: utf-8 -*-
"""Capas das aula-palestras — template reaproveitável entre eventos.

O rodapé (.capa-bar) traz a identificação ACADÊMICA do palestrante, não o evento.
Foi decisão do usuário (2026-09-06): "é assim que posso usar estas palestras em
outros eventos". Por isso o deck não fica preso ao NEEI/UERJ.

PARA LEVAR ESTAS PALESTRAS A OUTRO EVENTO, mude só o dicionário EVENTO abaixo
(rótulo do topo e faixa de logos) e, se for o caso, a lista AULAS. O rodapé
permanece igual — é a sua credencial, vale em qualquer lugar.

ATENÇÃO ÀS DATAS: o calendário publicado em
https://valantien.github.io/calendario-neei-uerj-2026/ está DESATUALIZADO.
O usuário informou em 2026-09-06 que a abertura passou para 01/10/2026.
As demais datas NÃO foram confirmadas — não inventar.
"""
import io, os, datetime, html

BASE = os.path.dirname(os.path.abspath(__file__))
DIAS = ["segunda-feira","terça-feira","quarta-feira","quinta-feira","sexta-feira","sábado","domingo"]

# ---------- o que é específico do evento (trocar tudo aqui para reusar) ----------
EVENTO = dict(
    rotulo="Módulo 5 — Fronteira Tecnológica",   # nome OFICIAL do módulo; o conteúdo vai no subtítulo
    logos="../assets/logos-neei-uerj.png",       # faixa institucional; None esconde a faixa
    logos_alt="UERJ · PPGECC · NEEI · PGCTIn · UFF · FEP · Universidade Pedagógica de Maputo",
)

# ---------- o rodapé: credencial acadêmica, igual em todos os eventos ----------
RODAPE = [
    ("Doutorando",        "Prof. Me. Krysamon D. B. Cavalcante"),
    ("Instituição",       "UFF — PGCTIn"),
    ("Orientação",        "Profª. Drª. Edicléa Mascarenhas Fernandes"),
    ("Grupo de Pesquisa", "Núcleo de Educação Especial e Inclusiva (NEEI)"),
    # "Data" removida do rodapé a pedido do usuário (2026-09-12); data_rodape ficou sem uso
]

# data=None  -> capa sai com marcador "[data a confirmar]"
# fundo="globo" -> globo de pontos animado (escolha do usuário para a aula 1, 2026-09-12);
# omitido      -> orbe estático
AULAS = [
 dict(n=1, arq="01-capa", data="2026-10-01", confirmada=True, fundo="globo",
      titulo="Competências Docentes para a Sociedade Digital", titulo_classe="title-long",
      sub="O que se espera dos professores numa educação mediada por tecnologias digitais e inteligência artificial?",
      profs=["Prof. Me. Krysamon D. B. Cavalcante"], data_rodape="Outubro/2026",
      logos_dados=("../assets/logos.png", "UNESCO · Cetic.br · NIC.br · CGI.br")),   # fontes dos dados, rotuladas
 dict(n=2, arq="capa-aula-2-iara", data=None, confirmada=False,
      titulo="Apresentando a I.A.R.A.",
      sub="Inteligência Artificial para Raras Assistência: objetivo, base de treinamento, e o lugar da supervisão humana",
      profs=["Prof. Me. Krysamon D. B. Cavalcante", "Cristina"], data_rodape="Setembro 2026"),
 dict(n=3, arq="capa-aula-3-workshop-1", data=None, confirmada=False,
      titulo="Workshop prático I.A.R.A.<br>Parte 1",
      sub="Prompting avançado para planos de adaptação e simulações clínico-pedagógicas de manejo em sala",
      profs=["Prof. Me. Krysamon D. B. Cavalcante", "Cristina"], data_rodape="Setembro 2026"),
 dict(n=4, arq="capa-aula-4-workshop-2", data=None, confirmada=False,
      titulo="Workshop prático I.A.R.A.<br>Parte 2",
      sub="Modelagem de intervenção com IA: prevalências de síndromes e guias práticos de acessibilidade",
      profs=["Prof. Me. Krysamon D. B. Cavalcante", "Cristina"], data_rodape="Setembro 2026"),
 dict(n=5, arq="capa-aula-5-oficina", data=None, confirmada=False,
      titulo="Oficina pedagógica<br>do Módulo I.A.R.A.",
      sub="Planos de lição adaptados, construídos em cooperação entre professores e a assistente virtual",
      profs=["Prof. Me. Krysamon D. B. Cavalcante", "Cristina"], data_rodape="Setembro 2026"),
 dict(n=6, arq="capa-aula-6-avaliativa", data=None, confirmada=False,
      titulo="Atividade prática<br>avaliativa",
      sub="Consulta à I.A.R.A. sobre uma condição rara, extração de adaptações e análise crítica cruzando com a CIF",
      profs=["Prof. Me. Krysamon D. B. Cavalcante", "Cristina"], data_rodape="Setembro 2026"),
]

PH = '<span class="ph">[{}]</span>'

def bloco_data(a):
    if not a["data"]:
        return (PH.format("data a confirmar"), PH.format("horário a confirmar"))
    d = datetime.date.fromisoformat(a["data"])
    nxt = d + datetime.timedelta(days=1)
    MES = ["janeiro","fevereiro","março","abril","maio","junho","julho",
           "agosto","setembro","outubro","novembro","dezembro"]
    ev = f'{d.day} de {MES[d.month-1]} de {d.year}<br>{DIAS[d.weekday()]}, 19h'
    tz = (f'🇧🇷 Brasil 19h00<br>🇲🇿 Moçambique 00h00 ({nxt.strftime("%d/%m")})')
    return ev, tz

TPL = io.open(os.path.join(BASE, "_capa-template.html"), encoding="utf-8").read()
GLOBO_JS = io.open(os.path.join(BASE, "_globo.js"), encoding="utf-8").read()
for _marca in ("{{FUNDO}}", "{{SCRIPT}}"):
    assert _marca in TPL, f"{_marca} sumiu do _capa-template.html"

def bloco_fundo(a):
    """Devolve (markup do fundo, <script>) conforme o fundo escolhido."""
    if a.get("fundo") == "globo":
        return ('<div class="globe-wrap"><div class="globe-glow"></div><canvas id="globe"></canvas></div>',
                f"<script>\n{GLOBO_JS}</script>")
    return '<div class="orb"></div>', ""

def bloco_rodape(a):
    cols = "".join(
        f'<div class="capa-bar-col"><span class="capa-bar-label">{html.escape(l)}</span>'
        f'<span class="capa-bar-value">{a["data_rodape"] if v is None else v}</span></div>'
        for l, v in RODAPE)
    return f'<div class="capa-bar">{cols}</div>'

def bloco_logos(a):
    """Faixa institucional (camada do evento)."""
    partes = []
    if EVENTO["logos"]:
        partes.append(f'<div class="card"><img src="{EVENTO["logos"]}" alt="{html.escape(EVENTO["logos_alt"])}"></div>')
    return f'<div class="logos">{"".join(partes)}</div>' if partes else ""

def bloco_dados(a):
    """Fontes dos dados da aula: canto inferior direito, sem caixa, com rótulo."""
    if not a.get("logos_dados"):
        return ""
    src, alt = a["logos_dados"]
    return (f'<div class="logos-dados"><span class="lbl">Dados:</span>'
            f'<img src="{src}" alt="{html.escape(alt)}"></div>')

for a in AULAS:
    _ev, _tz = bloco_data(a)
    quem = " · ".join(html.escape(p) for p in a["profs"])
    _fundo, _script = bloco_fundo(a)
    out = (TPL
        .replace("{{FUNDO}}", _fundo)
        .replace("{{SCRIPT}}", _script)
        # sem "Aula N de M": removido a pedido do usuário (2026-09-12)
        .replace("{{EYEBROW}}", EVENTO["rotulo"])
        .replace("{{TITULO}}", a["titulo"])
        .replace("{{TITLE_CLASS}}", a.get("titulo_classe", ""))
        .replace("{{SUB}}", a["sub"])
        .replace("{{QUEM}}", quem)
        .replace("{{RODAPE}}", bloco_rodape(a))
        .replace("{{LOGOS}}", bloco_logos(a))
        .replace("{{DADOS}}", bloco_dados(a))
        .replace("{{DOCTITLE}}", f'Capa — Módulo 5, aula {a["n"]}'))
    p = os.path.join(BASE, "..", a["arq"] + ".html")
    io.open(p, "w", encoding="utf-8").write(out)
    marca = "" if a["confirmada"] else "   ← data PENDENTE"
    print(f'  aula {a["n"]}: {a["arq"]}.html  ({a["data"] or "sem data"}){marca}')
