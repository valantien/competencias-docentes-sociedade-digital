# Geradores

O script é a fonte da verdade: para mudar dado ou layout, edite o script e rode
de novo. Não edite o HTML gerado à mão, porque a próxima execução sobrescreve a
alteração. Todos rodam de qualquer diretório (os caminhos são relativos ao
próprio arquivo).

| Script | Gera | Tela no deck | O que faz |
|---|---|---|---|
| `build-index.py` | `../../index.html` | todas | Funde as 37 telas (lista `ORDEM`) num deck só, escopando o CSS de cada uma por `#sNN`. Aplica o padrão do deck (fonte no rodapé, fontes embutidas). **Aborta** se houver `<div>` desbalanceado, imagem ou fonte ausente, ou JS com erro de sintaxe. `--fonte "Nome"` gera uma cópia de teste com outra fonte. |
| `gen-capas-modulo5.py` | `01-capa.html` + `capa-aula-2..6-*.html` | 1 | Capas a partir de `_capa-template.html`. O globo animado vem de `_globo.js`. Campos por aula: `fundo="globo"`, `logos_dados`, `data_rodape` (sem uso). A camada do evento fica em `EVENTO` e a credencial em `RODAPE`. |
| `gen-slide-21.py` | `fora-21-professores-apoio-situacoes-sensiveis.html` | 28 | Slope chart de 3 painéis × 6 séries, com desempilhamento automático de rótulos, num único `<svg>` 1:1 (1160×530). |
| `gen-slide-22.py` | `fora-22-escolas-convivencia-participativa.html` | 29 | Clona o slide 19 (tela 25) e calcula o afastamento lateral mínimo dos nós sobrepostos (`margin-left`), mantendo `left` no valor real. |
| `gen-slide-23a.py` | `25-54-formacao-continuada.html` | 30 | Destaque 54% + tendência 2021–2024. O "Total" é uma linha pêssego de 7px (`style` inline). |

## Como rodar

```bash
python3 "palestra_01/apresentacao/slides/generators/gen-capas-modulo5.py"
python3 "palestra_01/apresentacao/slides/generators/build-index.py"
```

Depois de regerar qualquer tela, rode o `build-index.py` para atualizar o deck.

## Atenção — dependência de template

`gen-slide-22.py` **lê o `slide-19-*.html` como template**. Se você alterar o
slide 19, corrija-o e só então regere o 22, nunca no mesmo comando. As trocas
de texto do gerador passam por `troca()`, que tem `assert`: se o trecho do slide
19 mudar, o script para com uma mensagem, em vez de gerar um slide 22
desalinhado sem avisar (isso aconteceu duas vezes, ver `MISTAKES.md`).

## Renumeração

`renumerar.py` mantém o prefixo `NN-` dos arquivos de tela igual à posição no deck (lista `ORDEM` do `build-index.py`). Rode `python3 renumerar.py` para ver o plano e `--aplicar` para executar, sempre que inserir, remover ou reordenar telas. Ele também reescreve os nomes nos outros geradores, neste README, no `AGENTS.md` e no `handoff.md`.
