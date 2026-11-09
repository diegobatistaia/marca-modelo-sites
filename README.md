# Molde de marcas (site + Instagram + Reels automáticos)

Este repositório é o **molde**: o sistema da Pixelzada pronto para uma marca
nova, sem conteúdo e sem nada escrito à mão. Cada marca nasce dele com o botão
verde **Use this template** e tem repositório, Instagram, chaves e projeto no
Claude próprios.

**Passo a passo completo, clique a clique:** [docs/GUIA-NOVA-MARCA.md](docs/GUIA-NOVA-MARCA.md).

## O que vem pronto

| Peça | Robô (GitHub Actions) | Código |
|---|---|---|
| Site de notícias (coleta, redação pela Routine, gate de qualidade, deploy) | Coletar, Finalizar, Deploy, Capas, Promover, Métricas | `scripts/engine/`, `scripts/pipeline/`, `templates/` |
| Carrosséis e Stories no Instagram | Instagram | `scripts/social/instagram.py`, `arte.py`, `pauta.py`, `templates/social/` |
| Motor de pesquisa de vídeos dos concorrentes | Pesquisa de vídeos | `scripts/social/pesquisa.py` |
| Robô do Telegram (links com um toque) | Telegram | `scripts/social/telegram.py` |
| Montagem dos Reels na identidade (20 molduras) | Montar Reels | `scripts/social/montagem.py`, `scripts/social/gerador/` |
| Fila e publicação de Reels | Reels | `scripts/social/reels.py`, `social/reels/fila.json` |
| Página "Gaveta de Reels" | (o Claude publica) | `scripts/social/gaveta.py` |
| Painel das marcas | Painel | `scripts/social/painel.py` (ramo `painel-dados`) |

## Os 3 arquivos que fazem a marca

1. **`marca.yaml`**: nome, domínio, @, hashtag, horários de carrossel e Reel,
   CTA, crédito, aviso legal, robô do Git, hospedagem.
2. **`social/pesquisa/config.yaml`**: concorrentes, temas (com o assunto do CTA
   e as hashtags), palavras bloqueadas, modo lançamento.
3. **`site.config.yaml`**: editorias, fontes de notícia, palavras da coleta,
   ritmo de matérias, regras de qualidade.

Mais a **identidade** (cores, fontes e logos com os mesmos nomes de arquivo;
lista no Apêndice A do guia) e as **3 skills** em `.claude/skills/`, que o
Claude reescreve para o tom e o nicho da marca.

## Chaves (GitHub > Settings > Secrets and variables > Actions)

| Secret | Para quê |
|---|---|
| `HOSTINGER_SSH_KEY` | enviar o site e as mídias para `<domínio>/ig/` |
| `INSTAGRAM_TOKEN` | publicar no Instagram |
| `META_TOKEN` | ler concorrentes (chave de Página do Facebook, nunca expira) |
| `TELEGRAM_TOKEN` | robô do Telegram |

Sem a chave, cada robô avisa e sai sem erro. Nunca escreva chave em arquivo.

## Comandos (na sessão do Claude)

    python scripts/tools/selfcheck.py              confere tudo (rode depois de cada mudança)
    python scripts/tools/logo_provisorio.py        logo provisório com o nome da marca
    python -m scripts.pipeline.run build           gera o site
    python -m scripts.social.instagram agenda      carrosséis de hoje
    python -m scripts.social.reels gaveta          quantos Reels há na fila
    python -m scripts.social.montagem automatico   monta os vídeos de social/reels/entrada/
    python -m scripts.social.painel                estado da marca para o painel
    python scripts/tools/onde_trocar.py <nome>     onde um nome antigo ainda aparece

Mais detalhes do Instagram: [social/INSTAGRAM.md](social/INSTAGRAM.md).

## Regras que valem para toda marca

- Repositório **público** (minutos grátis ilimitados no GitHub Actions; as chaves ficam nos Secrets).
- Contas, chaves, memória do Claude e Gaveta **separadas** por marca.
- CTA do Reel só convida a seguir: "Essa é a página pra seguir e acompanhar {assunto}".
- Matéria só com duas fontes independentes (ou o anúncio oficial da própria empresa).
- Mercado financeiro: `aviso_legal` obrigatório e nada de recomendar ativo.
- Melhoria nova entra primeiro aqui no molde e depois vai para cada marca.
