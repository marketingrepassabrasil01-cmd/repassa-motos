#!/usr/bin/env python3
"""Gera a versão de produção para o Vercel em dist/.

O projeto no Vercel não lê o GitHub, então publicamos só dois HTMLs e apontamos
imagens e data.js para o jsDelivr no commit exato (cache permanente, sem espera):

  dist/index.html            -> site/index.html (página de entrada)
  dist/catalogo/index.html   -> index.html (app do catálogo)

Uso: python3 scripts/build-prod.py [sha]   (padrão: HEAD)
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sha = sys.argv[1] if len(sys.argv) > 1 else subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
CDN = f"https://cdn.jsdelivr.net/gh/marketingrepassabrasil01-cmd/repassa-motos@{sha}/"

dist = ROOT / "dist"
(dist / "catalogo").mkdir(parents=True, exist_ok=True)

# Catálogo: imagens e dados pelo CDN, servido em /catalogo/
app = (ROOT / "index.html").read_text(encoding="utf-8")
app = app.replace('href="img/', f'href="{CDN}img/').replace('src="img/', f'src="{CDN}img/')
app = app.replace('<script src="data.js"></script>',
                  f'<script>window.IMG_BASE = "{CDN}";</script>\n<script src="{CDN}data.js"></script>')
(dist / "catalogo" / "index.html").write_text(app, encoding="utf-8")

# Site: imagens pelo CDN, links do catálogo para /catalogo/
site = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
site = site.replace('../img/', f'{CDN}img/').replace('href="../"', 'href="/catalogo/"')
(dist / "index.html").write_text(site, encoding="utf-8")

print(f"dist/ gerado para o commit {sha[:7]}")
