# Instagram da marca

Tudo sai sozinho. Os horários, o @, a hashtag, o CTA e o aviso legal ficam em
`marca.yaml`; os concorrentes e temas dos Reels em `social/pesquisa/config.yaml`.

| O quê | Quando | Onde se configura |
|---|---|---|
| Carrossel (+ Story) | `instagram.carrosseis.horarios` | `marca.yaml` |
| Reel de vídeo | `reels.horarios` (e `reels.grades` para mudar a partir de uma data) | `marca.yaml` |
| Lista de vídeos dos concorrentes | `coletas` (padrão 6h) | `social/pesquisa/config.yaml` |

## Como funciona

```
Carrosséis
  Routine da redação -> social/pautas/<slug>.json -> workflow Instagram:
  desenha (templates/social/) -> envia para <domínio>/ig/<slug>/ -> publica pela API

Reels
  workflow Pesquisa (6h) lê os concorrentes -> lista do dia -> baixa (yt-dlp)
  workflow Telegram (10 em 10 min) recebe links do dono -> baixa
  workflow Montar Reels -> moldura da marca (scripts/social/gerador/) -> social/reels/fila.json
  workflow Reels (10 em 10 min) -> envia para <domínio>/ig/ -> publica pela API
```

O Instagram só aceita mídia por link público: por isso todo post passa pela
pasta `/ig/` do site antes de ser publicado. Sem domínio com SSH, nada sai.

## Chaves (GitHub > Settings > Secrets and variables > Actions)

| Secret | Para quê |
|---|---|
| `INSTAGRAM_TOKEN` | publicar (API com login do Instagram, graph.instagram.com) |
| `META_TOKEN` | ler concorrentes (chave de Página do Facebook, nunca expira) |
| `TELEGRAM_TOKEN` | robô do Telegram (BotFather) |
| `HOSTINGER_SSH_KEY` | enviar o site e as mídias para a hospedagem |

Sem a chave, cada robô avisa no resumo e sai sem erro.

## Comandos úteis (na sessão do Claude)

    python -m scripts.social.instagram agenda     carrosséis de hoje
    python -m scripts.social.instagram check      confere as pautas
    python -m scripts.social.reels gaveta         quantos Reels há na fila
    python -m scripts.social.reels check          confere a fila
    python -m scripts.social.gaveta saida.html    página "Gaveta de Reels"
    python -m scripts.social.pesquisa lista       lista de vídeos do dia

Botões no GitHub (Actions > workflow > Run workflow): **Instagram > teste**
confere a chave; **Pesquisa de vídeos > teste** lê um concorrente;
**Pesquisa de vídeos > link** monta o Reel de um link.

O formato das pautas está em `.claude/skills/instagram/SKILL.md`.
