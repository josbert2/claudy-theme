#!/usr/bin/env python3
"""Servidor local del editor de colores de Claudy Theme.

Sirve theme-editor.html y, en POST /save, reescribe el tema elegido aplicando
el mapeo de colores sobre una copia pristina. Soporta los 4 temas.
Idempotente: cada guardado parte siempre de la base original del tema.

Uso:  python3 theme-editor-server.py   ->   http://localhost:7333/theme-editor.html
"""
import glob
import http.server
import json
import os
import re
import shutil
import socketserver

PORT = 7333
ROOT = os.path.dirname(os.path.abspath(__file__))
THEMES_DIR = os.path.join(ROOT, "themes")
THEMES = ["claudy-dark", "claudy-forest", "claudy-ocean", "claudy-minimal"]

# Snapshot pristino por tema (la primera vez).
for _t in THEMES:
    _src = os.path.join(THEMES_DIR, _t + ".json")
    _base = os.path.join(THEMES_DIR, "." + _t + ".base.json")
    if os.path.exists(_src) and not os.path.exists(_base):
        shutil.copy(_src, _base)


def theme_targets(theme):
    """Archivos a reescribir para un tema: el del repo y la copia instalada."""
    targets = [os.path.join(THEMES_DIR, theme + ".json")]
    pattern = os.path.expanduser(
        "~/.vscode/extensions/*claudy-dark*/themes/" + theme + ".json")
    targets.extend(glob.glob(pattern))
    return targets


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_POST(self):
        if self.path != "/save":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self.send_error(400)
            return
        theme = data.get("theme", "claudy-dark")
        if theme not in THEMES:           # whitelist: evita path traversal
            self.send_error(400, "tema desconocido")
            return
        mapping = {k.lower(): v.lower() for k, v in data.get("mapping", {}).items()}
        base = os.path.join(THEMES_DIR, "." + theme + ".base.json")
        text = open(base, encoding="utf-8").read()
        if mapping:
            pattern = "(" + "|".join(re.escape(k) for k in mapping) + ")"
            text = re.sub(
                pattern,
                lambda m: mapping[m.group(0).lower()],
                text,
                flags=re.IGNORECASE,
            )
        written = 0
        for target in theme_targets(theme):
            try:
                with open(target, "w", encoding="utf-8") as f:
                    f.write(text)
                written += 1
            except OSError:
                pass
        body = ('{"ok":true,"theme":"%s","written":%d}' % (theme, written)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as srv:
        print(f"Claudy theme editor -> http://localhost:{PORT}/theme-editor.html")
        srv.serve_forever()
