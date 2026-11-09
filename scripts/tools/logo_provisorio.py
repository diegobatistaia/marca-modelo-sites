"""Gera logos PROVISÓRIOS da marca a partir de marca.yaml (nome) e site.config.yaml (cores).

Serve para a marca nova rodar no primeiro dia, antes da identidade definitiva.
Quando o logo de verdade ficar pronto, substitua os arquivos com os MESMOS nomes.

    python scripts/tools/logo_provisorio.py

Escreve:
    assets/logo/logo-mono-preto.svg      texto preto (rodapé claro dos carrosséis)
    assets/logo/logo-transparente.svg    texto na cor da marca (fundos escuros)
    assets/logo/logo-claro.svg / logo-escuro.svg
    assets/logo/simbolo.svg / simbolo-destaque.svg / favicon.svg
    assets/logo/*.png e favicon.ico      ícones do site instalado
    scripts/social/gerador/              cópia dos SVGs usados nas molduras dos Reels
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts import marca as M  # noqa: E402
from scripts.engine import config as C  # noqa: E402

LOGO = ROOT / "assets" / "logo"
GERADOR = ROOT / "scripts" / "social" / "gerador"


def wordmark(texto: str, cor: str, fundo: str | None = None) -> str:
    largura = max(220, int(len(texto) * 40 + 60))
    rect = f'<rect width="{largura}" height="80" fill="{fundo}"/>' if fundo else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largura} 80" width="{largura}" height="80">'
            f'{rect}<text x="50%" y="58" text-anchor="middle" font-family="Anton, Impact, Arial Narrow, sans-serif" '
            f'font-size="56" letter-spacing="1" fill="{cor}">{escape(texto.upper())}</text></svg>\n')


def simbolo(letra: str, cor: str, fundo: str) -> str:
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">'
            f'<rect width="100" height="100" rx="18" fill="{fundo}"/>'
            f'<text x="50" y="72" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="66" '
            f'fill="{cor}">{escape(letra.upper())}</text></svg>\n')


def pngs(letra: str, cor: str, fundo: str) -> None:
    from PIL import Image, ImageDraw, ImageFont
    for nome, tam in (("icon-192.png", 192), ("icon-512.png", 512), ("icon-maskable-192.png", 192),
                      ("icon-maskable-512.png", 512), ("apple-touch-icon.png", 180)):
        img = Image.new("RGB", (tam, tam), fundo)
        d = ImageDraw.Draw(img)
        try:
            fonte = ImageFont.truetype(str(GERADOR / "fonts" / "f1.ttf"), int(tam * 0.62))
        except OSError:
            fonte = ImageFont.load_default()
        d.text((tam / 2, tam / 2), letra.upper(), fill=cor, font=fonte, anchor="mm")
        img.save(LOGO / nome)
    Image.open(LOGO / "icon-192.png").save(LOGO / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])


def main() -> int:
    cfg = C.load()
    nome = M.nome() or "Marca"
    cor, fundo = cfg.get("brand.primary", "#C6FF1A"), cfg.get("brand.ink", "#0B0A10")
    letra = nome.strip()[0]
    LOGO.mkdir(parents=True, exist_ok=True)
    arquivos = {
        "logo-mono-preto.svg": wordmark(nome, "#0B0A10"),
        "logo-transparente.svg": wordmark(nome, cor),
        "logo-claro.svg": wordmark(nome, "#0B0A10", "#FFFFFF"),
        "logo-escuro.svg": wordmark(nome, cor, fundo),
        "simbolo.svg": simbolo(letra, cor, fundo),
        "simbolo-destaque.svg": simbolo(letra, fundo, cor),
        "favicon.svg": simbolo(letra, cor, fundo),
    }
    for arq, svg in arquivos.items():
        (LOGO / arq).write_text(svg, encoding="utf-8")
    for arq in ("logo-mono-preto.svg", "logo-transparente.svg", "simbolo.svg"):
        shutil.copy(LOGO / arq, GERADOR / arq)
    pngs(letra, cor, fundo)
    print(f"logos provisórios de {nome!r} gravados em assets/logo/ e scripts/social/gerador/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
