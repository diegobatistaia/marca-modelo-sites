"""Ficha da marca (marca.yaml): a única fonte do que muda de uma marca para outra.

Uso no código:

    from scripts import marca
    marca.nome()        # "Marca Exemplo"
    marca.arroba()      # "@marcaexemplo"
    marca.get("reels.horarios")

Os nomes dos secrets são fixos no molde (cada marca tem o próprio repositório,
então não precisam de sufixo): INSTAGRAM_TOKEN, META_TOKEN, TELEGRAM_TOKEN e
HOSTINGER_SSH_KEY.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ARQUIVO = ROOT / "marca.yaml"

SECRET_INSTAGRAM = "INSTAGRAM_TOKEN"
SECRET_PESQUISA = "META_TOKEN"
SECRET_TELEGRAM = "TELEGRAM_TOKEN"


@lru_cache(maxsize=1)
def dados() -> dict:
    if not ARQUIVO.exists():
        raise FileNotFoundError("marca.yaml não encontrado na raiz do repositório")
    return yaml.safe_load(ARQUIVO.read_text(encoding="utf-8")) or {}


def get(caminho: str, padrao: Any = None) -> Any:
    no: Any = dados()
    for parte in caminho.split("."):
        if not isinstance(no, dict) or parte not in no:
            return padrao
        no = no[parte]
    return no


def nome() -> str:
    return get("marca.nome", "")


def usuario() -> str:
    return str(get("instagram.usuario", "")).lstrip("@")


def arroba() -> str:
    return f"@{usuario()}"


def dominio() -> str:
    return get("site.dominio", "")


def hashtag() -> str:
    tag = str(get("instagram.hashtag", "") or f"#{usuario().split('.')[0]}")
    return tag if tag.startswith("#") else f"#{tag}"


def aviso_legal() -> str:
    return str(get("marca.aviso_legal", "") or "").strip()


def cta(assunto: str) -> str:
    return str(get("reels.cta", "Essa é a página pra seguir e acompanhar {assunto}")).format(assunto=assunto)


def contexto() -> dict:
    """O que os templates (jinja) e o gerador de Reels recebem como `marca`."""
    return {
        "nome": nome(), "arroba": arroba(), "usuario": usuario(), "dominio": dominio(),
        "hashtag": hashtag(), "aviso_legal": aviso_legal(), "slogan": get("marca.slogan", ""),
    }


if __name__ == "__main__":
    import sys
    # python -m scripts.marca get bot.nome   -> imprime o valor (usado nos workflows)
    if len(sys.argv) == 3 and sys.argv[1] == "get":
        valor = get(sys.argv[2], "")
        print("" if valor is None else valor)
    else:
        print(contexto())
