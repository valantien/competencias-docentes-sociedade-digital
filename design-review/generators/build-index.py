# -*- coding: utf-8 -*-
"""Funde as telas aprovadas do design-review num único index.html apresentável.

Cada tela vira uma <section id="s-NN"> e TODO o CSS dela é reescrito com esse
prefixo. Sem isso o deck quebra: 113 dos 152 seletores se repetem entre arquivos
com definições diferentes (.stage em 33 arquivos, .m-src em 32, .row em 14).

Fonte da verdade: este script. Para mudar a ordem, editar ORDEM e rodar de novo.
"""
import io, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
DR   = os.path.join(BASE, "..")
OUT  = os.path.join(DR, "..", "index.html")

# Teste de fonte do texto: `--fonte "Roboto Condensed"` gera uma CÓPIA
# (index-teste-roboto-condensed.html) com essa fonte do Google Fonts no lugar da
# fonte do sistema. A Fraunces não muda. O index.html aprovado fica intacto.
# Funciona porque todas as telas do deck pegam a fonte do texto só pela variável --sans.
# Testadas em 2026-09-12: JetBrains Mono (recusada), Roboto Condensed (APROVADA —
# hoje é a fonte oficial do texto, definida no --sans de cada tela).
FONTE_TESTE = sys.argv[sys.argv.index("--fonte") + 1] if "--fonte" in sys.argv else None
FONTE_EXTRA = CSS_EXTRA = ""
if FONTE_TESTE:
    OUT = os.path.join(DR, "..", "index-teste-" + FONTE_TESTE.lower().replace(" ", "-") + ".html")
    FONTE_EXTRA = (f'<link href="https://fonts.googleapis.com/css2?family={FONTE_TESTE.replace(" ", "+")}'
                   f':wght@400;500;600;700&display=swap" rel="stylesheet">')
    CSS_EXTRA = f'.slide-sec{{--sans:"{FONTE_TESTE}",-apple-system,"Segoe UI",sans-serif !important}}'

ORDEM = [
 ("01-capa",                         "Capa"),
 ("02-disclaimer",                  "Esclarecimento inicial"),
 ("03-para-iniciar-a-conversa",                     "Para iniciar a conversa"),
 ("04-para-refletir",                     "Para refletir"),
 ("05-unesco-2008-fonte",                 "UNESCO 2008 — fonte"),
 ("06-unesco-2008",                   "UNESCO 2008"),
 ("07-unesco-2018-fonte",                 "UNESCO 2018 — fonte"),
 ("08-unesco-2018",                   "UNESCO 2018"),
 ("09-unesco-2024-fonte",                 "UNESCO 2024 — fonte"),
 ("10-unesco-2024",                   "UNESCO 2024"),
 ("11-ia-centrada-no-ser-humano",                         "IA centrada no ser humano"),
 ("12-linha-do-tempo-1984-2021",           "Linha do tempo 1984–2021"),
 ("13-linha-do-tempo-2021-2026",           "Linha do tempo 2021–2026"),
 ("14-usuarios-de-internet",     "Usuários de Internet"),
 ("15-acesso-so-por-celular",    "Acesso só por celular"),
 ("16-professores-e-celular","Professores e celular"),
 ("17-constatacao",                 "Constatação"),
 ("18-conectividade-significativa","Conectividade significativa"),
 ("19-nivel-de-conectividade",    "Nível de conectividade"),
 ("20-direitos-digitais",              "Direitos digitais"),
 ("21-relatorio-unesco-2023-fonte",                 "Relatório UNESCO 2023 — fonte"),
 ("22-relatorio-unesco-2023",                   "Relatório UNESCO 2023"),
 ("23-mec-saberes-digitais-fonte",                 "MEC Saberes Digitais — fonte"),
 ("24-saberes-digitais-docentes",         "Saberes digitais docentes"),
 ("25-54-formacao-continuada",          "54% — formação continuada"),
 ("26-temas-da-formacao",               "Temas da formação"),
 ("27-para-refletir-final",                     "Para refletir — final"),
 ("28-glossario",                   "Glossário"),
 ("29-referencias",                 "Referências"),
 ("30-sobre-o-palestrante",                          "Sobre o palestrante"),
]

def blocos_css(css):
    """Fatia o CSS em regras de topo, respeitando chaves aninhadas."""
    fora, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0: break
        sel = css[i:j].strip()
        d, k = 0, j
        while k < n:
            if css[k] == "{": d += 1
            elif css[k] == "}":
                d -= 1
                if d == 0: break
            k += 1
        fora.append((sel, css[j:k+1]))
        i = k + 1
    return fora

DESCARTAR = {"html", "body", "html,body", "html, body"}
keyframes = {}

def escopar(css, pid):
    saida = []
    for sel, corpo in blocos_css(css):
        s = re.sub(r"/\*.*?\*/", "", sel, flags=re.S).strip()
        if not s: continue
        if s.startswith("@keyframes"):
            keyframes[s] = corpo            # içado uma vez; todos são idênticos
            continue
        if s.startswith("@"):               # nenhum outro at-rule existe hoje
            saida.append(s + corpo); continue
        partes = []
        for p in s.split(","):
            p = p.strip()
            if not p: continue
            if p in DESCARTAR: continue
            if p == ":root": p = f"#{pid}"
            elif p == "*":   p = f"#{pid} *"
            else:            p = f"#{pid} {p}"
            partes.append(p)
        if partes:
            saida.append(", ".join(partes) + corpo)
    return "\n".join(saida)

css_tot, secoes, indice, imgs_reescritas, scripts_tela = [], [], [], [], []
for n, (arq, rotulo) in enumerate(ORDEM, start=1):
    pid = f"s{n:02d}"
    caminho = os.path.join(DR, arq + ".html")
    t = io.open(caminho, encoding="utf-8").read()
    css = re.search(r"<style>(.*?)</style>", t, re.S).group(1)
    corpo = re.search(r"<body>(.*?)</body>", t, re.S).group(1).strip()
    # trava: <div> desbalanceado numa tela fecha o palco (.deck-stage) antes da hora e
    # joga as telas seguintes para fora dele (aconteceu com a capa — ver MISTAKES.md)
    _html = re.sub(r"<script>.*?</script>", "", corpo, flags=re.S)
    _ab, _fe = len(re.findall(r"<div[\s>]", _html)), _html.count("</div>")
    if _ab != _fe:
        raise SystemExit(f"ABORTADO — {arq}.html tem <div> desbalanceado: abre {_ab}, fecha {_fe}")
    # Scripts da tela são PRESERVADOS (a capa com globo depende do seu).
    # Cada um precisa ser autocontido (IIFE) e é validado com node --check abaixo.
    scripts_tela += [(arq, js) for js in re.findall(r"<script>(.*?)</script>", corpo, re.S)]
    # As telas moram em design-review/ e apontam para ../assets/.
    # O index.html mora um nível acima, então o caminho tem de virar assets/.
    corpo, n_img = re.subn(r'(src|href)="\.\./assets/', r'\1="assets/', corpo)
    imgs_reescritas.append(n_img)
    css_tot.append(f"/* ===== {n:02d} · {arq} ===== */\n" + escopar(css, pid) +
                   f"\n#{pid} .stage{{box-shadow:none;border-radius:0}}")
    secoes.append(f'<section id="{pid}" class="slide-sec" data-rot="{rotulo}">\n{corpo}\n</section>')
    indice.append((n, rotulo))

SHELL_CSS = """
  *{box-sizing:border-box}
  html,body{height:100%;margin:0;background:#241B14;overflow:hidden}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
  .viewport{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;overflow:hidden}
  .deck-stage{position:relative;flex:0 0 auto;width:1280px;height:720px;transform-origin:center center;
    border-radius:6px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.45);background:#EFE3D1}
  /* font-family na seção: a regra body{font-family:var(--sans)} de cada tela é
     descartada na fusão; sem esta linha o texto herdaria a fonte do esqueleto. */
  .slide-sec{position:absolute;inset:0;opacity:0;visibility:hidden;transition:opacity .28s ease;
    font-family:var(--sans)}
  .slide-sec.on{opacity:1;visibility:visible}
  /* FONTE SEMPRE NO RODAPÉ (decisão do usuário, 2026-09-12): mesma posição em todas as telas.
     !important porque o CSS de cada tela vem escopado por #sNN (especificidade maior).
     A tela reserva o espaço do rodapé com padding-bottom; o gráfico (flex:1) absorve a diferença. */
  .slide-sec .m-src{position:absolute!important;left:60px!important;right:60px!important;
    bottom:18px!important;margin:0!important;z-index:5;
    font-size:.72rem!important;line-height:1.35!important}
  .slide-sec .stage:has(.m-src){padding-bottom:62px!important}
  .slide-sec > .stage{width:100%;height:100%}

  .hud{position:fixed;right:18px;bottom:16px;z-index:40;display:flex;align-items:center;gap:12px;
    background:rgba(30,27,24,.72);color:#EFE3D1;border-radius:999px;padding:8px 14px;
    font-size:.8rem;backdrop-filter:blur(6px)}
  .hud button{background:none;border:0;color:inherit;font:inherit;cursor:pointer;padding:2px 6px;border-radius:6px}
  .hud button:hover{background:rgba(255,255,255,.14)}
  .hud .rot{opacity:.72;max-width:230px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .progress{position:fixed;left:0;top:0;height:3px;background:#C1541F;z-index:50;transition:width .28s ease}

  .drawer{position:fixed;inset:0;z-index:60;background:rgba(30,27,24,.86);backdrop-filter:blur(4px);
    display:none;padding:44px;overflow:auto}
  .drawer.on{display:block}
  .drawer h2{color:#EFE3D1;font-size:.9rem;letter-spacing:.16em;text-transform:uppercase;margin-bottom:20px}
  .drawer ol{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:8px}
  .drawer li{color:#EFE3D1}
  .drawer button{width:100%;text-align:left;background:rgba(255,255,255,.06);border:0;color:inherit;
    font:inherit;padding:10px 14px;border-radius:8px;cursor:pointer;display:flex;gap:12px}
  .drawer button:hover{background:rgba(193,84,31,.35)}
  .drawer button.current{background:#C1541F;color:#FFF7EE;box-shadow:inset 4px 0 0 #F1B77F}
  .drawer button.current .n{opacity:1}
  .drawer .n{opacity:.5;min-width:26px}
  html:fullscreen, html:-webkit-full-screen{width:100%;height:100%;background:#241B14}
  ::backdrop{background:#241B14}
  @media print{.hud,.progress,.drawer{display:none!important}}
"""

SHELL_JS = """
const secs=[...document.querySelectorAll('.slide-sec')];
const TOTAL=secs.length;
const stage=document.querySelector('.deck-stage'), vp=document.querySelector('.viewport');
const prog=document.querySelector('.progress'), cont=document.querySelector('.cont'), rot=document.querySelector('.rot');
const idxButtons=[...document.querySelectorAll('.drawer button[data-go]')];
let cur=0;
function show(i){
  cur=Math.max(0,Math.min(TOTAL-1,i));
  secs.forEach((s,k)=>s.classList.toggle('on',k===cur));
  idxButtons.forEach(b=>{
    const active=+b.dataset.go===cur;
    b.classList.toggle('current',active);
    b.toggleAttribute('aria-current',active);
  });
  cont.textContent=(cur+1)+' / '+TOTAL;
  rot.textContent=secs[cur].dataset.rot;
  prog.style.width=((cur+1)/TOTAL*100)+'%';
  location.hash='#'+(cur+1);
}
/* Escala do palco.
   Não dependemos de eventos: 'resize' não dispara em alguns ambientes e a
   transição para tela cheia às vezes reporta dimensões antigas. Verificamos a
   cada quadro se as dimensões mudaram — é uma comparação de dois inteiros, e
   só tocamos no DOM quando algo realmente mudou. */
let _w=0, _h=0;
function fit(forcar){
  const d=document.documentElement;
  const w=d.clientWidth, h=d.clientHeight;
  if(!forcar && w===_w && h===_h) return;
  _w=w; _h=h;
  stage.style.transform='scale('+Math.min(w/1280, h/720)+')';
}
/* Dois vigias: rAF é suave e barato enquanto a aba está visível, mas o
   navegador o PAUSA quando a aba está oculta (medido: 0 quadros). O intervalo
   continua rodando nesse caso e custa uma comparação de inteiros 4x/s. */
(function vigia(){ fit(); requestAnimationFrame(vigia); })();
setInterval(fit, 250);
addEventListener('resize', ()=>fit(true));
for(const ev of ['fullscreenchange','webkitfullscreenchange']){
  addEventListener(ev, ()=>{ fit(true); requestAnimationFrame(()=>fit(true)); setTimeout(()=>fit(true),150); });
}
addEventListener('keydown',e=>{
  if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(cur+1)}
  else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(cur-1)}
  else if(e.key==='Home')show(0); else if(e.key==='End')show(TOTAL-1);
  else if(e.key.toLowerCase()==='f'&&e.ctrlKey&&e.shiftKey){e.preventDefault();toggleFS()}
  else if(e.key==='Escape')dr.classList.remove('on');
  else if(e.key==='i')dr.classList.toggle('on');
});
const dr=document.querySelector('.drawer');
document.querySelector('.btn-idx').onclick=()=>dr.classList.toggle('on');
document.querySelector('.btn-prev').onclick=()=>show(cur-1);
document.querySelector('.btn-next').onclick=()=>show(cur+1);
function toggleFS(){
  const d=document;
  if(d.fullscreenElement||d.webkitFullscreenElement){ (d.exitFullscreen||d.webkitExitFullscreen).call(d); }
  else { const e=d.documentElement; (e.requestFullscreen||e.webkitRequestFullscreen).call(e); }
}
document.querySelector('.btn-fs').onclick=toggleFS;
dr.querySelectorAll('button[data-go]').forEach(b=>b.onclick=()=>{show(+b.dataset.go);dr.classList.remove('on')});
show(Math.max(0,(parseInt(location.hash.slice(1))||1)-1));
"""

itens = "\n".join(
    f'      <li><button data-go="{n-1}"><span class="n">{n:02d}</span><span>{r}</span></button></li>'
    for n, r in indice)

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Competências Docentes para a Sociedade Digital — Módulo 5</title>
<!-- fontes embutidas (Fraunces + Roboto Condensed): o deck funciona sem internet -->
<link href="assets/fonts/fonts.css" rel="stylesheet">
{FONTE_EXTRA}
<style>
{SHELL_CSS}
{CSS_EXTRA}
/* ================= telas (CSS escopado por #sNN) ================= */
{chr(10).join(keyframes[k] and (k + keyframes[k]) for k in keyframes)}
{chr(10).join(css_tot)}
</style>
</head>
<body>

<div class="progress"></div>

<div class="viewport">
  <div class="deck-stage">
{chr(10).join(secoes)}
  </div>
</div>

<div class="hud">
  <button class="btn-idx" title="Índice (i)">☰</button>
  <span class="cont">1 / {len(ORDEM)}</span>
  <span class="rot"></span>
  <button class="btn-prev" title="Anterior (←)">‹</button>
  <button class="btn-next" title="Próxima (→)">›</button>
  <button class="btn-fs" title="Tela cheia (f)">⛶</button>
</div>

<div class="drawer">
  <h2>Índice — {len(ORDEM)} telas</h2>
  <ol>
{itens}
  </ol>
</div>

<script>
{SHELL_JS}
</script>
</body>
</html>
"""
# --- trava: toda imagem referenciada precisa existir a partir do index.html ---
_faltando = [u for u in sorted(set(re.findall(r'src="([^"]+)"', html)))
             if not u.startswith(("http", "data:"))
             and not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(OUT)), u))]
if _faltando:
    raise SystemExit("ABORTADO — imagens não encontradas a partir do index.html:\n  " + "\n  ".join(_faltando))

# --- trava: as fontes embutidas precisam existir (senão o deck cai na fonte do sistema sem avisar) ---
_fdir = os.path.join(os.path.dirname(os.path.abspath(OUT)), "assets", "fonts")
_fcss = os.path.join(_fdir, "fonts.css")
if not os.path.exists(_fcss):
    raise SystemExit("ABORTADO — assets/fonts/fonts.css não encontrado")
_ffalt = [u for u in re.findall(r"url\(([^)]+)\)", io.open(_fcss, encoding="utf-8").read())
          if not os.path.exists(os.path.join(_fdir, u))]
if _ffalt:
    raise SystemExit("ABORTADO — arquivos de fonte faltando:\n  " + "\n  ".join(_ffalt))

# --- trava: nunca escrever um deck com JS quebrado (já aconteceu uma vez) ---
import subprocess, tempfile, shutil
if shutil.which("node"):
    for _nome, _codigo in [("esqueleto", SHELL_JS)] + scripts_tela:
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(_codigo); _js = f.name
        r = subprocess.run(["node", "--check", _js], capture_output=True, text=True)
        os.unlink(_js)
        if r.returncode != 0:
            raise SystemExit(f"ABORTADO — erro de sintaxe no JS ({_nome}):\n" + r.stderr)

io.open(OUT, "w", encoding="utf-8").write(html)
print(f"{os.path.basename(OUT)} gerado: {len(ORDEM)} telas, {len(html)//1024} KB, {len(keyframes)} @keyframes içado(s)")
print(f"caminhos de mídia reescritos (../assets/ -> assets/): {sum(imgs_reescritas)}")
print(f"scripts de tela preservados: {len(scripts_tela)} ({', '.join(a for a, _ in scripts_tela) or 'nenhum'})")
