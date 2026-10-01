#!/usr/bin/env python3
"""Renomeia os arquivos de tela de design-review/ para a posição que têm no deck.

Nome novo = NN-<rótulo>.html, onde NN é a posição na lista ORDEM do build-index.py
e <rótulo> é o rótulo da tela, sem acento. Telas fora do deck ganham o prefixo "fora-".

Além de renomear os arquivos, o script reescreve os nomes antigos em: ORDEM,
os outros geradores, o README dos geradores, AGENTS.md e handoff.md.
MISTAKES.md é histórico e não é tocado.

Uso (sem argumento só mostra o plano; nada é alterado):
    python3 renumerar.py            # plano
    python3 renumerar.py --aplicar  # executa
Depois de aplicar, rode build-index.py: o index.html tem de sair idêntico.
Rode de novo sempre que inserir, remover ou reordenar telas em ORDEM.
"""
import ast, os, re, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
DR = os.path.dirname(AQUI)                                   # design-review/
RAIZ = os.path.abspath(os.path.join(DR, "..", "..", ".."))   # pasta do projeto
BUILD = os.path.join(AQUI, "build-index.py")
ALVOS_TEXTO = [BUILD] + [os.path.join(AQUI, f) for f in os.listdir(AQUI)
                         if f.endswith((".py", ".md")) and f not in ("renumerar.py", "build-index.py")] \
    + [os.path.join(RAIZ, "AGENTS.md"), os.path.join(RAIZ, "handoff.md")]


def slug(txt):
    s = unicodedata.normalize("NFKD", txt.replace("–", " ").replace("—", " ")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def ler_ordem():
    src = open(BUILD, encoding="utf-8").read()
    for no in ast.parse(src).body:
        if isinstance(no, ast.Assign) and getattr(no.targets[0], "id", "") == "ORDEM":
            return ast.literal_eval(no.value)
    sys.exit("ORDEM não encontrada em build-index.py")


def plano():
    ordem = ler_ordem()
    mapa, vistos = {}, set()
    for pos, (nome, rotulo) in enumerate(ordem, 1):
        novo = f"{pos:02d}-{slug(rotulo)}"
        assert novo not in vistos, f"rótulo repetido: {novo}"
        vistos.add(novo)
        mapa[nome] = novo
    noordem = {n for n, _ in ordem}
    for f in sorted(os.listdir(DR)):
        stem, ext = os.path.splitext(f)
        if ext != ".html" or stem in noordem or not re.match(r"(slide-|\d\d-)", stem):
            continue
        rest = re.sub(r"^(slide-)?(\d\d?[a-z]?-)?", "", stem)
        mapa[stem] = "fora-" + (re.sub(r"^slide-", "", stem) if stem.startswith("slide-") else rest)
    return {k: v for k, v in mapa.items() if k != v}


def main():
    mapa = plano()
    for k, v in mapa.items():
        print(f"  {k}.html  ->  {v}.html")
    print(f"{len(mapa)} arquivos a renomear")
    if "--aplicar" not in sys.argv:
        return
    for k in mapa:                                   # fase 1: nomes temporários
        os.rename(os.path.join(DR, k + ".html"), os.path.join(DR, k + ".html.tmp"))
    for k, v in mapa.items():                        # fase 2: nomes finais
        alvo = os.path.join(DR, v + ".html")
        assert not os.path.exists(alvo), alvo
        os.rename(os.path.join(DR, k + ".html.tmp"), alvo)
    padrao = re.compile(r"(?<![\w-])(" + "|".join(re.escape(k) for k in sorted(mapa, key=len, reverse=True)) + r")(?![\w-])")
    for p in ALVOS_TEXTO:
        s = open(p, encoding="utf-8").read()
        n = padrao.sub(lambda m: mapa[m.group(1)], s)
        if n != s:
            open(p, "w", encoding="utf-8").write(n)
            print("reescrito:", os.path.relpath(p, RAIZ))


if __name__ == "__main__":
    main()
